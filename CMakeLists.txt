cmake_minimum_required(VERSION 3.15...3.29)

project(SeismicMesh LANGUAGES C CXX)

##############################################################################

# CGAL and its components
find_package(CGAL REQUIRED)
message(STATUS "CGAL version: ${CGAL_VERSION}")

set(MIGRATION_SRCE "SeismicMesh/migration/cpp")
set(GENERATION_SRCE "SeismicMesh/generation/cpp")
set(SIZING_SRCE "SeismicMesh/sizing/cpp")
set(GEOMETRY_SRCE "SeismicMesh/geometry/cpp")

add_library(Common INTERFACE)
target_include_directories(Common INTERFACE ${MIGRATION_SRCE} ${GENERATION_SRCE} ${SIZING_SRC} ${GEOMETRY_SRCE})

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
message(STATUS "Found pybind11 v${pybind11_VERSION}: ${pybind11_INCLUDE_DIRS}")

pybind11_add_module(cpputils "${MIGRATION_SRCE}/cpputils.cpp")
target_link_libraries(cpputils PRIVATE Common CGAL::CGAL)
pybind11_add_module(FastHJ "${SIZING_SRCE}/FastHJ.cpp")
target_link_libraries(FastHJ PRIVATE Common CGAL::CGAL)
pybind11_add_module(delaunay "${GENERATION_SRCE}/delaunay.cpp")
target_link_libraries(delaunay PRIVATE Common CGAL::CGAL)
pybind11_add_module(delaunay_class "${GENERATION_SRCE}/delaunay_class.cpp")
target_link_libraries(delaunay_class PRIVATE Common CGAL::CGAL)
pybind11_add_module(delaunay_class3 "${GENERATION_SRCE}/delaunay_class3.cpp")
target_link_libraries(delaunay_class3 PRIVATE Common CGAL::CGAL)
pybind11_add_module(fast_geometry "${GEOMETRY_SRCE}/fast_geometry.cpp")
target_link_libraries(fast_geometry PRIVATE Common CGAL::CGAL)

install(TARGETS cpputils FastHJ delaunay delaunay_class delaunay_class3 fast_geometry LIBRARY DESTINATION SeismicMesh)
