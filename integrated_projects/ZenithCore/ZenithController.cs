// ZenithController.cs - Corrected Version
using System;
using System.Threading.Tasks;

namespace ZenithCoreSystem
{
    public class ZenithController
    {
        private readonly ZenithOptimizationSettings _settings;
        private bool _isRunning = false;

        public ZenithController() { _settings = new ZenithOptimizationSettings(); }
        public ZenithController(ZenithOptimizationSettings settings) { _settings = settings ?? new ZenithOptimizationSettings(); }

        public async Task<OptimizationResult> OptimizeAsync()
        {
            _isRunning = true;
            try
            {
                Console.WriteLine("[Zenith] Optimization running...");
                await Task.Delay(100);
                return new OptimizationResult { Success = true, Message = "OK", Timestamp = DateTime.UtcNow };
            }
            finally { _isRunning = false; }
        }

        public bool IsRunning => _isRunning;
        public ZenithOptimizationSettings Settings => _settings;
    }
}
