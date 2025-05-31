// file header include
#include "utils.h"

// system includes
#include <stdexcept>

// local includes
#include "nvapiwrapper.h"

//--------------------------------------------------------------------------------------------------

void assertSuccess(NvAPI_Status status, std::string_view error_prefix)
{
    if (status != NVAPI_OK)
    {
        NvApiWrapper nvapi;

        std::string error{error_prefix};
        error += " Error: " + nvapi.getErrorMessage(status);

        throw std::runtime_error(error);
    }
}
