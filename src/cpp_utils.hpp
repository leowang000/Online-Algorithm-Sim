#ifndef CPP_UTILS_HPP
#define CPP_UTILS_HPP

#include <iostream>

// Define the struct for the request
struct Request {
    uint32_t timestamp;
    uint64_t obj_id;
    uint32_t obj_size;
    int64_t next_access_vtime;  // -1 if no next access
};

#endif