
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "scheduler.hpp"

namespace py = pybind11;

PYBIND11_MODULE(utils, m) {
    // Bind the Result and Scheduler classes
    py::class_<Result>(m, "Result")
        .def_readwrite("total_requests", &Result::total_requests)
        .def_readwrite("unique_pages", &Result::unique_pages)
        .def_readwrite("cache_misses", &Result::cache_misses)
        .def(py::init<std :: vector<Request>&>());
}