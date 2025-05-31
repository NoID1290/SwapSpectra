#pragma once

// system includes
#include <string_view>

// local includes
#include "nvapiheaders.h"

//--------------------------------------------------------------------------------------------------

void assertSuccess(NvAPI_Status status, std::string_view error_prefix);
