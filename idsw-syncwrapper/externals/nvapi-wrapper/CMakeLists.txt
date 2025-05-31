#----------------------------------------------------------------------------------------------------------------------
# General settings
#----------------------------------------------------------------------------------------------------------------------

cmake_minimum_required(VERSION 3.27)
project(nvapiwrapper
        DESCRIPTION "Custom C++ bindings for as an internal dependency for other projects"
        HOMEPAGE_URL "https://github.com/FrogTheFrog/nvapi-wrapper"
        LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#----------------------------------------------------------------------------------------------------------------------
# Header files
#----------------------------------------------------------------------------------------------------------------------

set(HEADERS
    src/nvapiwrapper/nvapidrssession.h
    src/nvapiwrapper/nvapiheaders.h
    src/nvapiwrapper/nvapiwrapper.h
    src/nvapiwrapper/utils.h
    )

#----------------------------------------------------------------------------------------------------------------------
# Source files
#----------------------------------------------------------------------------------------------------------------------

set(SOURCES
    src/nvapiwrapper/nvapidrssession.cpp
    src/nvapiwrapper/nvapiwrapper.cpp
    src/nvapiwrapper/utils.cpp
    )

#----------------------------------------------------------------------------------------------------------------------
# Target settings
#----------------------------------------------------------------------------------------------------------------------

add_library(${PROJECT_NAME} ${HEADERS} ${SOURCES})
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/externals PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)
