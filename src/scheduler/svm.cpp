#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <unordered_map>
#include <vector>

#include "scheduler.hpp"

bool debug = false;

struct SVMScheduler : Scheduler {
    static const uint64_t kISVMCount = 2048;
    static const uint64_t kHistoryScale = 8;

    struct OPTGen {
        std::map<uint64_t, int64_t> last_access_time_;
        std::queue<std::map<uint64_t, int64_t>::iterator> access_queue_;
        std::vector<uint64_t> occupancy_;
        int64_t time_;
        const uint64_t cache_size_;

        OPTGen(uint64_t cache_size) : occupancy_(kHistoryScale * cache_size, 0), time_(-1), cache_size_(cache_size) {}

        bool IsOPTHit(uint64_t obj_id) {
            time_++;
            while (!access_queue_.empty() && access_queue_.front()->second + occupancy_.size() <= time_) {
                last_access_time_.erase(access_queue_.front());
                access_queue_.pop();
            }
            occupancy_[time_ % occupancy_.size()] = 0;
            auto it = last_access_time_.find(obj_id);
            if (it == last_access_time_.end()) {
                access_queue_.push(last_access_time_.emplace(obj_id, time_).first);
                return false;
            }
            for (uint64_t t = it->second % occupancy_.size(); ; t = (t + 1) % occupancy_.size()) {
                if (occupancy_[t] == cache_size_) {
                    return false;
                }
                if (t == time_ % occupancy_.size()) {
                    break;
                }
            }
            for (uint64_t t = it->second % occupancy_.size(); ; t = (t + 1) % occupancy_.size()) {
                occupancy_[t]++;
                if (t == time_ % occupancy_.size()) {
                    break;
                }
            }
            it->second = time_;
            return true;
        }
    };

    struct PCHR {
        static const uint64_t kMaxSize = 5;

        std::vector<uint64_t> regs_;

        void Insert(uint64_t obj_id) {
            auto it = std::find(regs_.begin(), regs_.end(), obj_id);
            if (it != regs_.end()) {
                regs_.erase(it);
            }
            regs_.insert(regs_.begin(), obj_id);
            if (regs_.size() > kMaxSize) {
                regs_.pop_back();
            }
        }
    };

    struct ISVM {
        static const uint64_t kWeightCount = 16;
        static const int64_t kThreshHold = 30;

        int8_t weights_[kWeightCount];

        ISVM() : weights_() {}

        static uint64_t Hash(uint64_t pc) {
            return ((pc >> 12) ^ (pc >> 16) ^ (pc >> 20) ^ (pc >> 24)) & (kWeightCount - 1);
        }
        
        int64_t Predict(const PCHR &pchr) const {
            int64_t res = 0;
            for (auto pc: pchr.regs_) {
                res += weights_[Hash(pc)];
            }
            return res;
        }

        void Update(const PCHR &pchr, bool is_opt_hit) {
            if (is_opt_hit) {
                for (auto pc: pchr.regs_) {
                    if (weights_[Hash(pc)] < kThreshHold) {
                        weights_[Hash(pc)]++;
                    }
                }
            } else {
                for (auto pc: pchr.regs_) {
                    if (weights_[Hash(pc)] > -kThreshHold) {
                        weights_[Hash(pc)]--;
                    }
                }
            }
        }
    };

    struct Cache {
        struct CacheLine {
            uint64_t obj_id_;
            int64_t friendliness_;
            int64_t last_access_time_;

            CacheLine(uint64_t obj_id, int64_t friendliness, int64_t last_access_time) : obj_id_(obj_id), friendliness_(friendliness), last_access_time_(last_access_time) {}

            bool operator<(const CacheLine &rhs) const {
                if (friendliness_ != rhs.friendliness_) {
                    return friendliness_ < rhs.friendliness_;
                }
                return last_access_time_ < rhs.last_access_time_;
            }
        };

        std::multiset<CacheLine> cache_;
        std::unordered_map<uint64_t, std::multiset<CacheLine>::iterator> obj_cache_map_;
        const uint64_t cache_size_;

        Cache(uint64_t cache_size) : cache_size_(cache_size) {}

        bool Contains(uint64_t obj_id) const {
            return obj_cache_map_.find(obj_id) != obj_cache_map_.end();
        }

        void Insert(uint64_t obj_id, int64_t friendliness, int64_t current_time) {
            auto it = obj_cache_map_.find(obj_id);
            if (it != obj_cache_map_.end()) {
                cache_.erase(it->second);
                it->second = cache_.emplace(obj_id, friendliness, current_time);
            } else {
                obj_cache_map_.emplace(obj_id, cache_.emplace(obj_id, friendliness, current_time));
            }
            if (cache_.size() > cache_size_) {
                obj_cache_map_.erase(cache_.begin()->obj_id_);
                cache_.erase(cache_.begin());
            }
        }
    };

    OPTGen opt_gen_;
    PCHR pchr_;
    ISVM isvm_table_[kISVMCount];
    Cache cache_;

    static uint64_t Hash(uint64_t pc) {
        return ((pc >> 12) ^ (pc >> 23) ^ (pc >> 34) ^ (pc >> 45)) & (kISVMCount - 1);
    }

    SVMScheduler(uint64_t cache_size) : Scheduler(cache_size), opt_gen_(cache_size), cache_(cache_size) {}

    Result run(std::vector<Request> &requests) {
        std::cout << "Total requests: " << requests.size() << std::endl;
        Result result(requests);
        uint64_t cnt = 0;
        // std::ofstream ofs("workspace/miss-time/prn0-svm.txt");
        for (const auto &request: requests) {
            if (cnt == 10) {
                debug = false;
            }
            if (cnt == requests.size() - 10) {
                debug = false;
            }
            if (cnt++ % (requests.size() / 100) == 0) {
                std::cout << "Processing " << (cnt / (requests.size() / 100)) << "%" << std::endl;
            }
            assert(opt_gen_.last_access_time_.size() <= OPTGen::kHistoryScale * cache_size);
            assert(opt_gen_.access_queue_.size() == opt_gen_.last_access_time_.size());
            assert(cache_.cache_.size() <= cache_size);
            assert(cache_.obj_cache_map_.size() == cache_.cache_.size());
            if (debug) {
                std::cout << "------------------------------" << std::endl;
                std::cout << "request obj_id: " << request.obj_id << std::endl;
                std::cout << "cache before replacing:" << std::endl;
                for (const auto &cache_line: cache_.cache_) {
                    std::cout << "\tobj_id: " << cache_line.obj_id_ << "\tfriendliness: " << cache_line.friendliness_ << std::endl;
                }
            }
            if (!cache_.Contains(request.obj_id)) {
                if (debug) {
                    std::cout << "cache miss" << std::endl;
                }
                result.cache_misses++;
            }
            int64_t friendliness = isvm_table_[Hash(request.obj_id)].Predict(pchr_);
            if (friendliness >= 60) {
                friendliness = 3;
            } else if (friendliness >= 0) {
                friendliness = 2;
            } else {
                friendliness = 1;
            }
            cache_.Insert(request.obj_id, friendliness, opt_gen_.time_ + 1);
            bool is_opt_hit = opt_gen_.IsOPTHit(request.obj_id);
            if (debug) {
                std::cout << "using isvm " << Hash(request.obj_id) << " to predict" << std::endl;
                std::cout << "predict result: " << friendliness << std::endl;
                std::cout << "cache after replacing:" << std::endl;
                for (const auto &cache_line: cache_.cache_) {
                    std::cout << "\tobj_id: " << cache_line.obj_id_ << "\tfriendliness: " << cache_line.friendliness_ << std::endl;
                }
                std::cout << "OPTgen output: " << (is_opt_hit ? "true" : "false") << std::endl;
                std::cout << "isvm before update:";
                for (auto w: isvm_table_[Hash(request.obj_id)].weights_) {
                    std::cout << (int) w << "\t";
                }
                std::cout << std::endl;
            }
            isvm_table_[Hash(request.obj_id)].Update(pchr_, is_opt_hit);
            if (debug) {
                std::cout << "isvm after update:";
                for (auto w: isvm_table_[Hash(request.obj_id)].weights_) {
                    std::cout << (int) w << "\t";
                }
                std::cout << std::endl;
                std::cout << "------------------------------" << std::endl;
            }
            pchr_.Insert(request.obj_id);
            // ofs << opt_gen_.time_ << "\t" << result.cache_misses << "\n";
        }
        return result;
    }
};

namespace py = pybind11;

PYBIND11_MODULE(svm, m) {
    py::class_<SVMScheduler>(m, "SVM")
        .def(py::init<const uint64_t>())
        .def("run", &SVMScheduler::run);
}