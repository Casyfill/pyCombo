cmake_minimum_required(VERSION 3.15...3.30)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(
    _combo
    src/Binder.cpp
    src/Combo/Graph.cpp
    src/Combo/Combo.cpp
)

target_include_directories(_combo PRIVATE src)

install(TARGETS _combo DESTINATION pycombo)
