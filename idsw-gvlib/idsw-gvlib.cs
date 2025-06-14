using System;
using System.IO;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Text.RegularExpressions;
using System.Text;

namespace NvngxUpdaterLib
{
    [ComVisible(true)]
    [Guid("EF37F47E-5204-4A7F-8CF5-C6A4C5E24BCD")] // Generate a new GUID
    public class NvngxUpdater
    {
        [DllImport("kernel32.dll")]
        private static extern IntPtr LoadLibrary(string dllPath);

        [DllImport("kernel32.dll")]
        private static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

        [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
        private delegate uint GetVersionDelegate();

        private const string NVNGX_BASE_PATH = @"C:\ProgramData\NVIDIA\NGX\models";
        private const string VERSION_FUNCTION = "NVSDK_NGX_GetSnippetVersion";

        public static void UpdateNvngxDll(string dllPath)
        {
            dllPath = dllPath.Trim().Trim('"');
            var fileName = Path.GetFileName(dllPath);

            // Validate and extract DLL type
            var dllType = ExtractDllType(fileName);
            if (string.IsNullOrEmpty(dllType))
            {
                Console.WriteLine($"Error: Invalid DLL type from filename: {fileName}");
                return;
            }

            // Verify DLL existence
            if (!File.Exists(dllPath))
            {
                Console.WriteLine($"Error: DLL not found at {dllPath}");
                return;
            }

            // Get DLL version info
            var version = GetDllVersion(dllPath);
            if (version == 0)
            {
                return;
            }

            var versionString = FormatVersion(version);
            var destPath = GetDestinationPath(dllType, version);
            var configPath = Path.Combine(NVNGX_BASE_PATH, "nvngx_config.txt");

            // Confirm operations
            DisplayOperationSummary(dllType, versionString, destPath, configPath);

            if (File.Exists(destPath))
            {
                Console.WriteLine("Error: Destination file already exists.");
                return;
            }

            // Execute update
            try
            {
                Directory.CreateDirectory(Path.GetDirectoryName(destPath));
                File.Copy(dllPath, destPath);
                UpdateConfig(configPath, dllType, "app_E658703", versionString);
                Console.WriteLine("NVNGX DLL update completed successfully.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error during update: {ex.Message}");
            }
        }

        private static string ExtractDllType(string fileName)
        {
            if (!fileName.Contains("_"))
                return null;

            var baseName = fileName.Split('_')[1].Replace(".dll", "");
            var validTypes = new[] { "dlss", "dlssg", "dlssd" };

            foreach (var type in validTypes)
            {
                if (baseName.StartsWith(type))
                    return type;
            }

            return null;
        }

        private static uint GetDllVersion(string dllPath)
        {
            var hModule = LoadLibrary(dllPath);
            if (hModule == IntPtr.Zero)
            {
                Console.WriteLine("Error: Failed to load DLL");
                return 0;
            }

            var procAddress = GetProcAddress(hModule, VERSION_FUNCTION);
            if (procAddress == IntPtr.Zero)
            {
                Console.WriteLine($"Error: Failed to get {VERSION_FUNCTION} function address");
                return 0;
            }

            var getVersion = Marshal.GetDelegateForFunctionPointer<GetVersionDelegate>(procAddress);
            return getVersion();
        }

        private static string FormatVersion(uint version)
        {
            var major = (version >> 16) & 0xFFFF;
            var minor = (version >> 8) & 0xFF;
            var patch = version & 0xFF;
            return $"{major}.{minor}.{patch}";
        }

        private static string GetDestinationPath(string dllType, uint version)
        {
            return Path.Combine(NVNGX_BASE_PATH, dllType, "versions", version.ToString(), "files", "160_E658703.bin");
        }

        private static void DisplayOperationSummary(string dllType, string version, string destPath, string configPath)
        {
            Console.WriteLine($"\nDLL Type: {dllType}");
            Console.WriteLine($"Version: {version}");
            Console.WriteLine($"\nOperations to perform:");
            Console.WriteLine($"1. Copy to: {destPath}");
            Console.WriteLine($"2. Update config: {configPath}");
        }

        private static void UpdateConfig(string path, string section, string key, string value)
        {
            var lines = File.Exists(path) ? File.ReadAllLines(path) : Array.Empty<string>();
            var newLines = new List<string>();
            var inSection = false;
            var sectionExists = false;
            var keyUpdated = false;

            foreach (var line in lines)
            {
                if (line.TrimStart().StartsWith("["))
                {
                    inSection = line.Trim() == $"[{section}]";
                    if (inSection) sectionExists = true;
                }
                else if (inSection && Regex.IsMatch(line, $@"^\s*{key}\s*="))
                {
                    newLines.Add($"{key} = {value}");
                    keyUpdated = true;
                    continue;
                }
                newLines.Add(line);
            }

            if (!sectionExists)
                newLines.Add($"[{section}]");
            if (!keyUpdated)
                newLines.Add($"{key} = {value}");

            File.WriteAllLines(path, newLines);
        }
    }
}
// This code provides a class NvngxUpdater that can be used to update NVIDIA NGX DLLs.
// It includes methods to validate the DLL type, get the version, copy the DLL to the correct location, and update a configuration file.

namespace ClearNVGX
    {
    [ComVisible(true)]
    [Guid("A1B2C3D4-E5F6-7890-1234-56789ABCDEF0")] // Generate a new GUID
    public class ClearNvngx
    {
        public static void ClearNvngxModels()
        {
            var modelsPath = @"C:\ProgramData\NVIDIA\NGX\models";
            if (Directory.Exists(modelsPath))
            {
                try
                {
                    Directory.Delete(modelsPath, true);
                    Console.WriteLine("NVNGX models cleared successfully.");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error clearing NVNGX models: {ex.Message}");
                }
            }
            else
            {
                Console.WriteLine("NVNGX models directory does not exist.");
            }
        }
    }
}
// This code provides a class ClearNvngx that can be used to clear the NVIDIA NGX models directory.
// It includes a method to delete the directory and handle any exceptions that may occur during the process.

namespace ReturnPresence
{
    [ComVisible(true)]
    [Guid("12345678-1234-1234-1234-123456789012")] // Generate a new GUID
    public class ReturnPresence
    {
        public static string GetPresence()
        {
            return "NVIDIA NGX Updater is running.";
        }
    }
}

// This code provides a class ReturnPresence that can be used to return a presence message indicating that the NVIDIA NGX Updater is running.

namespace NvApiCall
{
    [ComVisible(true)]
    [Guid("87654321-4321-4321-4321-210987654321")] // Generate a new GUID
    public class NvapiWrapper
    {
        private const string NVAPI_DLL = "nvapi64.dll";
        private static IntPtr nvApiModule;

        [DllImport("kernel32.dll")]
        private static extern IntPtr LoadLibrary(string dllPath);

        [DllImport("kernel32.dll")]
        private static extern IntPtr GetProcAddress(IntPtr hModule, string procName);

        [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
        private delegate NvAPI_Status NvAPI_InitializeDelegate();

        [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
        private delegate NvAPI_Status NvAPI_UnloadDelegate();

        [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
        private delegate NvAPI_Status NvAPI_GetInterfaceVersionStringDelegate(StringBuilder version);

        private static NvAPI_InitializeDelegate nvAPI_Initialize;
        private static NvAPI_UnloadDelegate nvAPI_Unload;
        private static NvAPI_GetInterfaceVersionStringDelegate nvAPI_GetInterfaceVersionString;

        private static readonly string[] POTENTIAL_PATHS = new[]
        {
            @"C:\Windows\System32\nvapi64.dll",
            @"C:\Windows\SysWOW64\nvapi64.dll",
            @"C:\Windows\System32\nvapi.dll"
        };

        public enum NvAPI_Status
        {
            OK = 0,
            ERROR = -1,
            LIBRARY_NOT_FOUND = -2,
            NO_IMPLEMENTATION = -3,
            API_NOT_INITIALIZED = -4,
            INVALID_ARGUMENT = -5,
            NVIDIA_DEVICE_NOT_FOUND = -6,
            END_ENUMERATION = -7,
            INVALID_HANDLE = -8,
            INCOMPATIBLE_STRUCT_VERSION = -9
        }

        private static T GetDelegateForFunction<T>(string functionName) where T : Delegate
        {
            IntPtr procAddress = GetProcAddress(nvApiModule, functionName);
            if (procAddress == IntPtr.Zero)
                throw new EntryPointNotFoundException($"Function {functionName} not found in NVAPI");

            return Marshal.GetDelegateForFunctionPointer<T>(procAddress);
        }

        private static void LoadNvApiFunctions()
        {
            nvAPI_Initialize = GetDelegateForFunction<NvAPI_InitializeDelegate>("NvAPI_Initialize");
            nvAPI_Unload = GetDelegateForFunction<NvAPI_UnloadDelegate>("NvAPI_Unload");
            nvAPI_GetInterfaceVersionString = GetDelegateForFunction<NvAPI_GetInterfaceVersionStringDelegate>("NvAPI_GetInterfaceVersionString");
        }

        private static string GetNvapiPath()
        {
            foreach (var path in POTENTIAL_PATHS)
            {
                if (File.Exists(path))
                    return path;
            }
            throw new FileNotFoundException("NVAPI DLL could not be found in expected locations.");
        }

        public static bool Initialize()
        {
            try
            {
                if (nvApiModule != IntPtr.Zero)
                    return true; // Already initialized

                string nvapiPath = GetNvapiPath();
                nvApiModule = LoadLibrary(nvapiPath);
                
                if (nvApiModule == IntPtr.Zero)
                    throw new DllNotFoundException($"Failed to load NVAPI from {nvapiPath}");

                LoadNvApiFunctions();
                
                var status = nvAPI_Initialize();
                if (status != NvAPI_Status.OK)
                    throw new InvalidOperationException($"NVAPI initialization failed with status: {status}");

                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"NVAPI initialization error: {ex.Message}");
                return false;
            }
        }

        public static void Unload()
        {
            try
            {
                if (nvApiModule != IntPtr.Zero)
                {
                    nvAPI_Unload();
                    nvApiModule = IntPtr.Zero;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"NVAPI unload error: {ex.Message}");
            }
        }

        public static string GetVersion()
        {
            try
            {
                if (!Initialize())
                    return null;

                var sb = new StringBuilder(64);
                var status = nvAPI_GetInterfaceVersionString(sb);
                
                if (status != NvAPI_Status.OK)
                    throw new InvalidOperationException($"Failed to get NVAPI version. Status: {status}");

                return sb.ToString();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error getting NVAPI version: {ex.Message}");
                return null;
            }
        }
    }
}
// This code provides a class NvapiWrapper that wraps NVAPI calls for initialization, unloading, and getting the version of the NVAPI library.


namespace WinGammaRamp
{
    [ComVisible(true)]
    [Guid("11223344-5566-7788-99AA-BBCCDDEEFF00")] // Generate a new GUID
    public class WindowsContrastBrightness
    {
        [DllImport("user32.dll")]
        private static extern bool SetDeviceGammaRamp(IntPtr hdc, ref GammaRamp lpGammaRamp);
        [DllImport("user32.dll")]
        private static extern IntPtr GetDC(IntPtr hWnd);
        [DllImport("user32.dll")]
        private static extern bool ReleaseDC(IntPtr hWnd, IntPtr hdc);
        public struct GammaRamp
        {
            public ushort[] Red;
            public ushort[] Green;
            public ushort[] Blue;
            public GammaRamp(int size)
            {
                Red = new ushort[size];
                Green = new ushort[size];
                Blue = new ushort[size];
            }
        }
        public static void SetContrastBrightness(float contrast, float brightness)
        {
            var ramp = new GammaRamp(256);
            for (int i = 0; i < 256; i++)
            {
                var value = (ushort)(Math.Clamp((i - 128) * contrast + 128 + brightness, 0, 255) * 65535 / 255);
                ramp.Red[i] = value;
                ramp.Green[i] = value;
                ramp.Blue[i] = value;
            }
            IntPtr hdc = GetDC(IntPtr.Zero);
            if (hdc != IntPtr.Zero)
            {
                SetDeviceGammaRamp(hdc, ref ramp);
                ReleaseDC(IntPtr.Zero, hdc);
            }
        }
    }
}
// This code provides a class WindowsContrastBrightness that allows setting the contrast and brightness for the display using P/Invoke to call Windows API functions.
// It uses a gamma ramp to adjust the pixel values based on the specified contrast and brightness levels.
// The gamma ramp is applied to the display device context obtained from the Windows API, allowing for real-time adjustments to the display settings.






