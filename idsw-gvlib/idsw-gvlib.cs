using System;
using System.IO;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Text.RegularExpressions;


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

namespace readGsyncStatus
    {
    [ComVisible(true)]
    [Guid("A1B2C3D4-E5F6-7890-1234-56789ABCDEF1")] // Generate a new GUID
    public class ReadGsyncStatus
    {
        public static string GetGsyncStatus()
        {
            // Placeholder for actual G-Sync status retrieval logic
            return "G-Sync is enabled.";
        }
    }
}


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



