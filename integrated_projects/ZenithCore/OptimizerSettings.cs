// ZenithCore Settings - Corrected Version
using System;

namespace ZenithCoreSystem
{
    public class ZenithOptimizationSettings
    {
        public int QmlRetryCount { get; set; } = 3;
        public int QmlBaseDelayMilliseconds { get; set; } = 500;
        public double ComplianceThreshold { get; set; } = 0.9;
        public bool SimulateQmlFailure { get; set; } = false;
        public string? RedisConnectionString { get; set; }
    }

    public class OptimizationResult
    {
        public bool Success { get; set; }
        public string Message { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
    }
}

namespace ZenithCoreSystem.Core
{
    public class OptimizerSettings
    {
        public int QmlRetryCount { get; set; } = 3;
        public int QmlBaseDelayMilliseconds { get; set; } = 500;
        public double ComplianceThreshold { get; set; } = 0.9;
        public bool SimulateQmlFailure { get; set; } = true;
        public string? RedisConnectionString { get; set; }
    }
}
