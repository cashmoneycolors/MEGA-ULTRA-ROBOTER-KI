using System;
using MegaUltra.Networking;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Net.Http;
using System.Text.Json;
using System.Text;
using System.Diagnostics;
using System.IO;
using System.Linq;
using Microsoft.Extensions.Logging;
using System.Net.NetworkInformation;

/// <summary>
/// 🔐🌐⚖️ ERWEITERTE NETZWERK-KOMPONENTEN - MAXIMALE VERNETZUNG 🔐🌐⚖️
/// Security Monitor, Load Balancer und weitere kritische vernetzte Komponenten
/// </summary>

// ===============================
// 🛡️ SECURITY MONITOR NETZWERK-KOMPONENTE
// ===============================
public class SecurityMonitorNetworkComponent : INetworkComponent
{
    public string ComponentId => "SecurityMonitor_" + Environment.MachineName;
    public string ComponentType => "SecurityMonitor";
    public ComponentStatus Status { get; private set; } = ComponentStatus.Stopped;
    
    private readonly ILogger _logger;
    private readonly Dictionary<string, int> _suspiciousIPs = new Dictionary<string, int>();
    private readonly Dictionary<string, DateTime> _lastSecurityEvents = new Dictionary<string, DateTime>();
    private readonly List<SecurityThreat> _detectedThreats = new List<SecurityThreat>();
    
    public event EventHandler<ComponentEventArgs> OnComponentEvent;
    
    public class SecurityThreat
    {
        public string Id { get; set; } = Guid.NewGuid().ToString();
        public string Type { get; set; }
        public string Source { get; set; }
        public string Description { get; set; }
        public DateTime DetectedAt { get; set; }
        public ThreatLevel Level { get; set; }
        public bool IsResolved { get; set; }
    }
    
    public enum ThreatLevel { Low, Medium, High, Critical }
    
    public SecurityMonitorNetworkComponent()
    {
        _logger = LoggerFactory.Create(builder => builder.AddConsole()).CreateLogger<SecurityMonitorNetworkComponent>();
    }
    
    public async Task Initialize()
    {
        try
        {
            Status = ComponentStatus.Starting;
            _logger.LogInformation("🛡️ Security Monitor Netzwerk-Komponente wird initialisiert...");
            
            // Starte kontinuierliche Sicherheitsüberwachung
            _ = Task.Run(ContinuousSecurityMonitoring);
            
            Status = ComponentStatus.Running;
            
            OnComponentEvent?.Invoke(this, new ComponentEventArgs
            {
                ComponentId = ComponentId,
                EventType = "SecurityMonitorStarted",
                Data = new Dictionary<string, object>
                {
                    { "MonitoringActive", true },
                    { "ThreatDetectionEnabled", true }
                }
            });
            
            _logger.LogInformation("✅ Security Monitor Netzwerk-Komponente erfolgreich initialisiert");
        }
        catch (Exception ex)
        {
            Status = ComponentStatus.Error;
            _logger.LogError(ex, "❌ Security Monitor Initialisierung fehlgeschlagen");
            throw;
        }
    }
    
    private async Task ContinuousSecurityMonitoring()
    {
        while (Status == ComponentStatus.Running)
        {
            try
            {
                // Netzwerk-Anomalien erkennen
                await DetectNetworkAnomalies();
                
                // Verdächtige Aktivitäten scannen
                await ScanForSuspiciousActivity();
                
                // System-Integrität prüfen
                await CheckSystemIntegrity();
                
                await Task.Delay(TimeSpan.FromSeconds(30));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Kontinuierliche Sicherheitsüberwachung Fehler");
                await Task.Delay(TimeSpan.FromMinutes(1));
            }
        }
    }
    
    private async Task DetectNetworkAnomalies()
    {
        try
        {
            // Netzwerk-Verbindungen analysieren
            var tcpConnections = IPGlobalProperties.GetIPGlobalProperties().GetActiveTcpConnections();
            var suspiciousConnections = tcpConnections
                .Where(c => c.LocalEndPoint.Port != 3000 && c.LocalEndPoint.Port != 3001 && 
                           c.LocalEndPoint.Port != 11434 && c.LocalEndPoint.Port > 1024)
                .ToList();
            
            if (suspiciousConnections.Count > 50) // Threshold für verdächtige Anzahl
            {
                var threat = new SecurityThreat
                {
                    Type = "NetworkAnomaly",
                    Source = "NetworkAnalysis",
                    Description = $"Ungewöhnlich hohe Anzahl an Netzwerk-Verbindungen: {suspiciousConnections.Count}",
                    DetectedAt = DateTime.UtcNow,
                    Level = ThreatLevel.Medium
                };
                
                await HandleSecurityThreat(threat);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Netzwerk-Anomalie-Erkennung fehlgeschlagen");
        }
    }
    
    private async Task ScanForSuspiciousActivity()
    {
        try
        {
            // Prüfe auf ungewöhnliche Prozesse
            var processes = Process.GetProcesses();
            var suspiciousProcesses = processes
                .Where(p => p.ProcessName.ToLower().Contains("hack") || 
                           p.ProcessName.ToLower().Contains("crack") ||
                           p.ProcessName.ToLower().Contains("keylog"))
                .ToList();
            
            foreach (var suspiciousProcess in suspiciousProcesses)
            {
                var threat = new SecurityThreat
                {
                    Type = "SuspiciousProcess",
                    Source = suspiciousProcess.ProcessName,
                    Description = $"Verdächtiger Prozess erkannt: {suspiciousProcess.ProcessName} (PID: {suspiciousProcess.Id})",
                    DetectedAt = DateTime.UtcNow,
                    Level = ThreatLevel.High
                };
                
                await HandleSecurityThreat(threat);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Verdächtige Aktivitäten-Scan fehlgeschlagen");
        }
    }
    
    private async Task CheckSystemIntegrity()
    {
        try
        {
            // Prüfe kritische System-Dateien
            var criticalFiles = new[]
            {
                Path.Combine(Environment.GetEnvironmentVariable("MEGA_ULTRA_PATH") ?? ".", "AI_CORE", "MegaUltraAIIntegrator.cs"),
                Path.Combine(Environment.GetEnvironmentVariable("MEGA_ULTRA_PATH") ?? ".", "server", "opengazai-server-enhanced.js")
            };
            
            foreach (var file in criticalFiles)
            {
                if (!File.Exists(file))
                {
                    var threat = new SecurityThreat
                    {
                        Type = "FileIntegrity",
                        Source = file,
                        Description = $"Kritische Datei fehlt oder wurde manipuliert: {file}",
                        DetectedAt = DateTime.UtcNow,
                        Level = ThreatLevel.Critical
                    };
                    
                    await HandleSecurityThreat(threat);
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "System-Integritäts-Check fehlgeschlagen");
        }
    }
    
    private async Task HandleSecurityThreat(SecurityThreat threat)
    {
        _detectedThreats.Add(threat);
        
        _logger.LogWarning($"🚨 SECURITY THREAT DETECTED: {threat.Type} - {threat.Description}");
        
        OnComponentEvent?.Invoke(this, new ComponentEventArgs
        {
            ComponentId = ComponentId,
            EventType = "ThreatDetected",
            Data = new Dictionary<string, object>
            {
                { "ThreatId", threat.Id },
                { "ThreatType", threat.Type },
                { "Description", threat.Description },
                { "Level", threat.Level.ToString() },
                { "Source", threat.Source },
                { "DetectedAt", threat.DetectedAt }
            }
        });
        
        // Automatische Gegenmaßnahmen bei kritischen Bedrohungen
        if (threat.Level == ThreatLevel.Critical)
        {
            await ExecuteEmergencyResponse(threat);
        }
    }
    
    private async Task ExecuteEmergencyResponse(SecurityThreat threat)
    {
        _logger.LogError($"🆘 CRITICAL THREAT - Executing emergency response for: {threat.Description}");
        
        OnComponentEvent?.Invoke(this, new ComponentEventArgs
        {
            ComponentId = ComponentId,
            EventType = "EmergencyResponseActivated",
            Data = new Dictionary<string, object>
            {
                { "ThreatId", threat.Id },
                { "ResponseType", "EmergencyLockdown" },
                { "Timestamp", DateTime.UtcNow }
            }
        });
    }
    
    public async Task<bool> ProcessMessage(NetworkMessage message)
    {
        try
        {
            _logger.LogDebug($"📨 Security Monitor verarbeitet Nachricht: {message.MessageType}");
            
            switch (message.MessageType)
            {
                case "ReportSuspiciousIP":
                    return await HandleSuspiciousIP(message);
                
                case "SecurityAlert":
                    return await HandleSecurityAlert(message);
                
                case "GetThreatReport":
                    return await HandleGetThreatReport(message);
                
                case "ClearThreats":
                    return await HandleClearThreats(message);
                
                default:
                    return false;
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Nachricht-Verarbeitung fehlgeschlagen: {message.MessageType}");
            return false;
        }
    }
    
    private async Task<bool> HandleSuspiciousIP(NetworkMessage message)
    {
        var ip = message.Data.GetValueOrDefault("ip", "").ToString();
        var reason = message.Data.GetValueOrDefault("reason", "").ToString();
        
        if (!string.IsNullOrEmpty(ip))
        {
            _suspiciousIPs[ip] = _suspiciousIPs.GetValueOrDefault(ip, 0) + 1;
            
            if (_suspiciousIPs[ip] > 5) // Schwellenwert
            {
                var threat = new SecurityThreat
                {
                    Type = "SuspiciousIP",
                    Source = ip,
                    Description = $"IP {ip} zeigt verdächtige Aktivitäten: {reason}",
                    DetectedAt = DateTime.UtcNow,
                    Level = ThreatLevel.Medium
                };
                
                await HandleSecurityThreat(threat);
            }
        }
        
        return true;
    }
    
    private async Task<bool> HandleSecurityAlert(NetworkMessage message)
    {
        var alertType = message.Data.GetValueOrDefault("alertType", "").ToString();
        var description = message.Data.GetValueOrDefault("description", "").ToString();
        var source = message.Data.GetValueOrDefault("source", message.FromNodeId).ToString();
        
        var threat = new SecurityThreat
        {
            Type = alertType,
            Source = source,
            Description = description,
            DetectedAt = DateTime.UtcNow,
            Level = Enum.Parse<ThreatLevel>(message.Data.GetValueOrDefault("level", "Medium").ToString())
        };
        
        await HandleSecurityThreat(threat);
        return true;
    }
    
    private async Task<bool> HandleGetThreatReport(NetworkMessage message)
    {
        var threatReport = new
        {
            TotalThreats = _detectedThreats.Count,
            ActiveThreats = _detectedThreats.Count(t => !t.IsResolved),
            RecentThreats = _detectedThreats.Where(t => t.DetectedAt > DateTime.UtcNow.AddHours(-24)).ToList(),
            SuspiciousIPs = _suspiciousIPs,
            ThreatsByLevel = _detectedThreats.GroupBy(t => t.Level).ToDictionary(g => g.Key.ToString(), g => g.Count())
        };
        
        OnComponentEvent?.Invoke(this, new ComponentEventArgs
        {
            ComponentId = ComponentId,
            EventType = "ThreatReportGenerated",
            Data = new Dictionary<string, object>
            {
                { "Report", threatReport },
                { "RequestId", message.Id }
            }
        });
        
        return true;
    }
    
    private async Task<bool> HandleClearThreats(NetworkMessage message)
    {
        var clearedCount = _detectedThreats.Count;
        _detectedThreats.Clear();
        _suspiciousIPs.Clear();
        
        _logger.LogInformation($"🧹 {clearedCount} Bedrohungen wurden gelöscht");
        
        OnComponentEvent?.Invoke(this, new ComponentEventArgs
        {
            ComponentId = ComponentId,
            EventType = "ThreatsCleared",
            Data = new Dictionary<string, object>
            {
                { "ClearedCount", clearedCount },
                { "Timestamp", DateTime.UtcNow }
            }
        });
        
        return true;
    }
    
    public async Task<NetworkMessage> CreateStatusMessage()
    {
        return new NetworkMessage
        {
            ComponentType = ComponentType,
            MessageType = "ComponentStatus",
            Data = GetStatus()
        };
    }
    
    public Dictionary<string, object> GetStatus()
    {
        return new Dictionary<string, object>
        {
            { "ComponentId", ComponentId },
            { "Status", Status.ToString() },
            { "TotalThreats", _detectedThreats.Count },
            { "ActiveThreats", _detectedThreats.Count(t => !t.IsResolved) },
            { "SuspiciousIPCount", _suspiciousIPs.Count },
            { "MonitoringActive", Status == ComponentStatus.Running },
            { "Capabilities", new[] { "ThreatDetection", "NetworkMonitoring", "IntegrityChecking", "EmergencyResponse" } }
        };
    }
    
    public async Task Shutdown()
    {
        Status = ComponentStatus.Stopped;
        _logger.LogInformation("🛑 Security Monitor Netzwerk-Komponente heruntergefahren");
    }
}

// ===============================
// ⚖️ LOAD BALANCER NETZWERK-KOMPONENTE
// ===============================
public class LoadBalancerNetworkComponent : INetworkComponent
{
    public string ComponentId => "LoadBalancer_" + Environment.MachineName;
    public string ComponentType => "LoadBalancer";
    public ComponentStatus Status { get; private set; } = ComponentStatus.Stopped;
    
    private readonly ILogger _logger;
    private readonly MegaUltraNetworkOrchestrator _orchestrator;
    private readonly Dictionary<string, NodeLoadInfo> _nodeLoads = new Dictionary<string, NodeLoadInfo>();
    private readonly Queue<PendingRequest> _requestQueue = new Queue<PendingRequest>();
    
    public event EventHandler<ComponentEventArgs> OnComponentEvent;
    
    public class NodeLoadInfo
    {
        public string NodeId { get; set; }
        public double CpuUsage { get; set; }
        public double MemoryUsage { get; set; }
        public int ActiveRequests { get; set; }
        public double ResponseTime { get; set; }
        public DateTime LastUpdate { get; set; }
        public bool IsAvailable => LastUpdate > DateTime.UtcNow.AddSeconds(-30);
    }
    
    public class PendingRequest
    {
        public string Id { get; set; } = Guid.NewGuid().ToString();
        public string RequestType { get; set; }
        public Dictionary<string, object> Data { get; set; }
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public int Priority { get; set; } = 0;
        public string PreferredNodeType { get; set; }
    }
    
    public LoadBalancerNetworkComponent(MegaUltraNetworkOrchestrator orchestrator)
    {
        _orchestrator = orchestrator;
        _logger = LoggerFactory.Create(builder => builder.AddConsole()).CreateLogger<LoadBalancerNetworkComponent>();
    }
    
    public async Task Initialize()
    {
        try
        {
            Status = ComponentStatus.Starting;
            _logger.LogInformation("⚖️ Load Balancer Netzwerk-Komponente wird initialisiert...");
            
            // Starte Load-Monitoring
            _ = Task.Run(ContinuousLoadMonitoring);
            
            // Starte Request-Processing
            _ = Task.Run(ProcessRequestQueue);
            
            Status = ComponentStatus.Running;
            
            OnComponentEvent?.Invoke(this, new ComponentEventArgs
            {
                ComponentId = ComponentId,
                EventType = "LoadBalancerStarted",
                Data = new Dictionary<string, object>
                {
                    { "QueueProcessing", true },
                    { "LoadMonitoring", true }
                }
            });
            
            _logger.LogInformation("✅ Load Balancer Netzwerk-Komponente erfolgreich initialisiert");
        }
        catch (Exception ex)
        {
            Status = ComponentStatus.Error;
            _logger.LogError(ex, "❌ Load Balancer Initialisierung fehlgeschlagen");
            throw;
        }
    }
    
    private async Task ContinuousLoadMonitoring()
    {
        while (Status == ComponentStatus.Running)
        {
            try
            {
                // Sammle Load-Informationen von allen Nodes
                await CollectNodeLoadInformation();
                
                // Analysiere Load-Verteilung
                await AnalyzeLoadDistribution();
                
                await Task.Delay(TimeSpan.FromSeconds(10));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Load-Monitoring Fehler");
                await Task.Delay(TimeSpan.FromSeconds(30));
            }
        }
    }
    
    private async Task CollectNodeLoadInformation()
    {
        // Request Load-Information von allen verfügbaren Nodes
        await _orchestrator.SendMessage(new NetworkMessage
        {
            MessageType = "LoadBalanceRequest",
            Data = new Dictionary<string, object>
            {
                { "RequestType", "GetLoadInfo" },
                { "RequiresResponse", true }
            }
        });
    }
    
    private async Task AnalyzeLoadDistribution()
    {
        var availableNodes = _nodeLoads.Values.Where(n => n.IsAvailable).ToList();
        
        if (availableNodes.Any())
        {
            var avgCpuUsage = availableNodes.Average(n => n.CpuUsage);
            var avgMemoryUsage = availableNodes.Average(n => n.MemoryUsage);
            
            // Identifiziere überlastete Nodes
            var overloadedNodes = availableNodes.Where(n => 
                n.CpuUsage > avgCpuUsage * 1.5 || n.MemoryUsage > avgMemoryUsage * 1.5).ToList();
            
            if (overloadedNodes.Any())
            {
                OnComponentEvent?.Invoke(this, new ComponentEventArgs
                {
                    ComponentId = ComponentId,
                    EventType = "LoadImbalanceDetected",
                    Data = new Dictionary<string, object>
                    {
                        { "OverloadedNodes", overloadedNodes.Select(n => n.NodeId).ToList() },
                        { "AvgCpuUsage", avgCpuUsage },
                        { "AvgMemoryUsage", avgMemoryUsage }
                    }
                });
                
                // Starte Load-Umverteilung
                await RedistributeLoad(overloadedNodes, availableNodes.Except(overloadedNodes).ToList());
            }
        }
    }
    
    private async Task RedistributeLoad(List<NodeLoadInfo> overloadedNodes, List<NodeLoadInfo> availableNodes)
    {
        _logger.LogInformation($"⚖️ Starte Load-Umverteilung: {overloadedNodes.Count} überlastete Nodes");
        
        foreach (var overloadedNode in overloadedNodes)
        {
            var bestTargetNode = availableNodes
                .OrderBy(n => n.CpuUsage + n.MemoryUsage)
                .FirstOrDefault();
            
            if (bestTargetNode != null)
            {
                await _orchestrator.SendMessage(new NetworkMessage
                {
                    ToNodeId = overloadedNode.NodeId,
                    MessageType = "LoadBalanceRedirect",
                    Data = new Dictionary<string, object>
                    {
                        { "TargetNodeId", bestTargetNode.NodeId },
                        { "RedirectPercentage", 50 } // 50% der Last umleiten
                    }
                });
                
                _logger.LogInformation($"⚖️ Load-Umleitung: {overloadedNode.NodeId} → {bestTargetNode.NodeId}");
            }
        }
    }
    
    private async Task ProcessRequestQueue()
    {
        while (Status == ComponentStatus.Running)
        {
            try
            {
                PendingRequest request = null;
                lock (_requestQueue)
                {
                    if (_requestQueue.Count > 0)
                    {
                        request = _requestQueue.Dequeue();
                    }
                }
                
                if (request != null)
                {
                    await ProcessLoadBalancedRequest(request);
                }
                else
                {
                    await Task.Delay(100);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Request-Queue Verarbeitung fehlgeschlagen");
                await Task.Delay(1000);
            }
        }
    }
    
    private async Task ProcessLoadBalancedRequest(PendingRequest request)
    {
        try
        {
            // Finde besten verfügbaren Node für Request
            var bestNode = FindBestNodeForRequest(request);
            
            if (bestNode != null)
            {
                await _orchestrator.SendMessage(new NetworkMessage
                {
                    ToNodeId = bestNode.NodeId,
                    MessageType = request.RequestType,
                    Data = request.Data,
                    Priority = request.Priority
                });
                
                bestNode.ActiveRequests++;
                
                OnComponentEvent?.Invoke(this, new ComponentEventArgs
                {
                    ComponentId = ComponentId,
                    EventType = "RequestRouted",
                    Data = new Dictionary<string, object>
                    {
                        { "RequestId", request.Id },
                        { "TargetNode", bestNode.NodeId },
                        { "RequestType", request.RequestType }
                    }
                });
            }
            else
            {
                _logger.LogWarning($"⚖️ Kein verfügbarer Node für Request {request.Id}");
                
                // Request zurück in Queue (mit Delay)
                await Task.Delay(5000);
                lock (_requestQueue)
                {
                    _requestQueue.Enqueue(request);
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Load-Balanced Request Verarbeitung fehlgeschlagen: {request.Id}");
        }
    }
    
    private NodeLoadInfo FindBestNodeForRequest(PendingRequest request)
    {
        var availableNodes = _nodeLoads.Values.Where(n => n.IsAvailable).ToList();
        
        if (!availableNodes.Any()) return null;
        
        // Filtere nach bevorzugtem Node-Type falls angegeben
        if (!string.IsNullOrEmpty(request.PreferredNodeType))
        {
            var preferredNodes = availableNodes.Where(n => 
                n.NodeId.Contains(request.PreferredNodeType, StringComparison.OrdinalIgnoreCase)).ToList();
            
            if (preferredNodes.Any())
                availableNodes = preferredNodes;
        }
        
        // Berechne Score für jeden Node (niedrigster Score = bester Node)
        var scoredNodes = availableNodes.Select(node => new
        {
            Node = node,
            Score = CalculateNodeScore(node, request)
        }).OrderBy(x => x.Score);
        
        return scoredNodes.FirstOrDefault()?.Node;
    }
    
    private double CalculateNodeScore(NodeLoadInfo node, PendingRequest request)
    {
        // Score basierend auf CPU, Memory, aktiven Requests und Response-Time
        var cpuScore = node.CpuUsage * 0.4;
        var memoryScore = node.MemoryUsage * 0.3;
        var requestScore = node.ActiveRequests * 0.2;
        var responseTimeScore = node.ResponseTime * 0.1;
        
        return cpuScore + memoryScore + requestScore + responseTimeScore;
    }
    
    public async Task<bool> ProcessMessage(NetworkMessage message)
    {
        try
        {
            _logger.LogDebug($"📨 Load Balancer verarbeitet Nachricht: {message.MessageType}");
            
            switch (message.MessageType)
            {
                case "LoadBalanceRequest":
                    return await HandleLoadBalanceRequest(message);
                
                case "LoadBalanceResponse":
                    return await HandleLoadBalanceResponse(message);
                
                case "QueueRequest":
                    return await HandleQueueRequest(message);
                
                case "GetQueueStatus":
                    return await HandleGetQueueStatus(message);
                
                default:
                    return false;
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Nachricht-Verarbeitung fehlgeschlagen: {message.MessageType}");
            return false;
        }
    }
    
    private async Task<bool> HandleLoadBalanceRequest(NetworkMessage message)
    {
        var requestType = message.Data.GetValueOrDefault("RequestType", "").ToString();
        
        if (requestType == "QueueRequest")
        {
            var pendingRequest = new PendingRequest
            {
                RequestType = message.Data.GetValueOrDefault("TargetMessageType", "").ToString(),
                Data = message.Data.GetValueOrDefault("RequestData", new Dictionary<string, object>()) as Dictionary<string, object>,
                Priority = Convert.ToInt32(message.Data.GetValueOrDefault("Priority", 0)),
                PreferredNodeType = message.Data.GetValueOrDefault("PreferredNodeType", "").ToString()
            };
            
            lock (_requestQueue)
            {
                _requestQueue.Enqueue(pendingRequest);
            }
            
            _logger.LogDebug($"⚖️ Request in Queue eingereiht: {pendingRequest.Id}");
        }
        
        return true;
    }
    
    private async Task<bool> HandleLoadBalanceResponse(NetworkMessage message)
    {
        // Update Node-Load-Information
        if (message.Data.TryGetValue("CpuUsage", out var cpuUsageObj) &&
            double.TryParse(cpuUsageObj.ToString(), out var cpuUsage))
        {
            var nodeLoad = new NodeLoadInfo
            {
                NodeId = message.FromNodeId,
                CpuUsage = cpuUsage,
                MemoryUsage = Convert.ToDouble(message.Data.GetValueOrDefault("MemoryUsage", 0)),
                ActiveRequests = Convert.ToInt32(message.Data.GetValueOrDefault("ActiveRequests", 0)),
                ResponseTime = Convert.ToDouble(message.Data.GetValueOrDefault("ResponseTime", 0)),
                LastUpdate = DateTime.UtcNow
            };
            
            _nodeLoads[message.FromNodeId] = nodeLoad;
            
            _logger.LogDebug($"⚖️ Node-Load aktualisiert: {message.FromNodeId} (CPU: {cpuUsage:F1}%)");
        }
        
        return true;
    }
    
    private async Task<bool> HandleQueueRequest(NetworkMessage message)
    {
        return await HandleLoadBalanceRequest(message);
    }
    
    private async Task<bool> HandleGetQueueStatus(NetworkMessage message)
    {
        var queueStatus = new
        {
            QueueLength = _requestQueue.Count,
            ActiveNodes = _nodeLoads.Values.Count(n => n.IsAvailable),
            TotalNodes = _nodeLoads.Count,
            AverageCpuUsage = _nodeLoads.Values.Where(n => n.IsAvailable).DefaultIfEmpty().Average(n => n?.CpuUsage ?? 0),
            AverageMemoryUsage = _nodeLoads.Values.Where(n => n.IsAvailable).DefaultIfEmpty().Average(n => n?.MemoryUsage ?? 0)
        };
        
        OnComponentEvent?.Invoke(this, new ComponentEventArgs
        {
            ComponentId = ComponentId,
            EventType = "QueueStatusReported",
            Data = new Dictionary<string, object>
            {
                { "QueueStatus", queueStatus },
                { "RequestId", message.Id }
            }
        });
        
        return true;
    }
    
    public async Task<NetworkMessage> CreateStatusMessage()
    {
        return new NetworkMessage
        {
            ComponentType = ComponentType,
            MessageType = "ComponentStatus",
            Data = GetStatus()
        };
    }
    
    public Dictionary<string, object> GetStatus()
    {
        var availableNodes = _nodeLoads.Values.Where(n => n.IsAvailable).ToList();
        
        return new Dictionary<string, object>
        {
            { "ComponentId", ComponentId },
            { "Status", Status.ToString() },
            { "QueueLength", _requestQueue.Count },
            { "ActiveNodes", availableNodes.Count },
            { "TotalNodes", _nodeLoads.Count },
            { "AverageCpuUsage", availableNodes.DefaultIfEmpty().Average(n => n?.CpuUsage ?? 0) },
            { "AverageMemoryUsage", availableNodes.DefaultIfEmpty().Average(n => n?.MemoryUsage ?? 0) },
            { "Capabilities", new[] { "LoadBalancing", "RequestQueuing", "NodeMonitoring", "AutoScaling" } }
        };
    }
    
    public async Task Shutdown()
    {
        Status = ComponentStatus.Stopped;
        _logger.LogInformation("🛑 Load Balancer Netzwerk-Komponente heruntergefahren");
    }
}

// ===============================
// 📊 METRICS COLLECTOR NETZWERK-KOMPONENTE
// ===============================
public class MetricsCollectorNetworkComponent : INetworkComponent
{
    public string ComponentId => "MetricsCollector_" + Environment.MachineName;
    public string ComponentType => "MetricsCollector";
    public ComponentStatus Status { get; private set; } = ComponentStatus.Stopped;
    
    private readonly ILogger _logger;
    private readonly Dictionary<string, List<MetricData>> _metricsHistory = new Dictionary<string, List<MetricData>>();
    private readonly object _metricsLock = new object();
    
    public event EventHandler<ComponentEventArgs> OnComponentEvent;
    
    public class MetricData
    {
        public string MetricName { get; set; }
        public double Value { get; set; }
        public DateTime Timestamp { get; set; }
        public string Source { get; set; }
        public Dictionary<string, string> Labels { get; set; } = new Dictionary<string, string>();
    }
    
    public MetricsCollectorNetworkComponent()
    {
        _logger = LoggerFactory.Create(builder => builder.AddConsole()).CreateLogger<MetricsCollectorNetworkComponent>();
    }
    
    public async Task Initialize()
    {
        try
        {
            Status = ComponentStatus.Starting;
            _logger.LogInformation("📊 Metrics Collector Netzwerk-Komponente wird initialisiert...");
            
            // Starte Metriken-Sammlung
            _ = Task.Run(ContinuousMetricsCollection);
            
            Status = ComponentStatus.Running;
            
            OnComponentEvent?.Invoke(this, new ComponentEventArgs
            {
                ComponentId = ComponentId,
                EventType = "MetricsCollectorStarted",
                Data = new Dictionary<string, object>
                {
                    { "CollectionActive", true },
                    { "HistoryRetention", "24h" }
                }
            });
            
            _logger.LogInformation("✅ Metrics Collector Netzwerk-Komponente erfolgreich initialisiert");
        }
        catch (Exception ex)
        {
            Status = ComponentStatus.Error;
            _logger.LogError(ex, "❌ Metrics Collector Initialisierung fehlgeschlagen");
            throw;
        }
    }
    
    private async Task ContinuousMetricsCollection()
    {
        while (Status == ComponentStatus.Running)
        {
            try
            {
                await CollectSystemMetrics();
                await CleanupOldMetrics();
                await Task.Delay(TimeSpan.FromSeconds(60)); // Jede Minute
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Metriken-Sammlung Fehler");
                await Task.Delay(TimeSpan.FromMinutes(1));
            }
        }
    }
    
    private async Task CollectSystemMetrics()
    {
        var timestamp = DateTime.UtcNow;
        
        // System-Metriken sammeln
        var metrics = new List<MetricData>
        {
            new MetricData
            {
                MetricName = "system_cpu_usage",
                Value = GetCpuUsage(),
                Timestamp = timestamp,
                Source = ComponentId
            },
            new MetricData
            {
                MetricName = "system_memory_usage",
                Value = GetMemoryUsage(),
                Timestamp = timestamp,
                Source = ComponentId
            },
            new MetricData
            {
                MetricName = "network_connections",
                Value = GetNetworkConnectionCount(),
                Timestamp = timestamp,
                Source = ComponentId
            }
        };
        
        // Metriken speichern
        foreach (var metric in metrics)
        {
            StoreMetric(metric);
        }
        
        // Metriken an andere Komponenten senden
        OnComponentEvent?.Invoke(this, new ComponentEventArgs
        {
            ComponentId = ComponentId,
            EventType = "MetricsCollected",
            Data = new Dictionary<string, object>
            {
                { "Metrics", metrics },
                { "Timestamp", timestamp }
            }
        });
    }
    
    private void StoreMetric(MetricData metric)
    {
        lock (_metricsLock)
        {
            if (!_metricsHistory.ContainsKey(metric.MetricName))
            {
                _metricsHistory[metric.MetricName] = new List<MetricData>();
            }
            
            _metricsHistory[metric.MetricName].Add(metric);
        }
    }
    
    private async Task CleanupOldMetrics()
    {
        var cutoff = DateTime.UtcNow.AddHours(-24); // 24h Retention
        
        lock (_metricsLock)
        {
            foreach (var kvp in _metricsHistory.ToList())
            {
                var filteredMetrics = kvp.Value.Where(m => m.Timestamp > cutoff).ToList();
                if (filteredMetrics.Count != kvp.Value.Count)
                {
                    _metricsHistory[kvp.Key] = filteredMetrics;
                    _logger.LogDebug($"📊 Alte Metriken bereinigt: {kvp.Key}");
                }
            }
        }
    }
    
    private double GetCpuUsage()
    {
        try
        {
            using var process = Process.GetCurrentProcess();
            return Math.Min(100, process.TotalProcessorTime.TotalMilliseconds / Environment.TickCount * 100);
        }
        catch
        {
            return 0.0;
        }
    }
    
    private double GetMemoryUsage()
    {
        try
        {
            return GC.GetTotalMemory(false) / 1024.0 / 1024.0; // MB
        }
        catch
        {
            return 0.0;
        }
    }
    
    private double GetNetworkConnectionCount()
    {
        try
        {
            return IPGlobalProperties.GetIPGlobalProperties().GetActiveTcpConnections().Length;
        }
        catch
        {
            return 0.0;
        }
    }
    
    public async Task<bool> ProcessMessage(NetworkMessage message)
    {
        try
        {
            _logger.LogDebug($"📨 Metrics Collector verarbeitet Nachricht: {message.MessageType}");
            
            switch (message.MessageType)
            {
                case "StoreMetric":
                    return await HandleStoreMetric(message);
                
                case "GetMetrics":
                    return await HandleGetMetrics(message);
                
                case "GetMetricsHistory":
                    return await HandleGetMetricsHistory(message);
                
                default:
                    return false;
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Nachricht-Verarbeitung fehlgeschlagen: {message.MessageType}");
            return false;
        }
    }
    
    private async Task<bool> HandleStoreMetric(NetworkMessage message)
    {
        try
        {
            var metricName = message.Data.GetValueOrDefault("metricName", "").ToString();
            var value = Convert.ToDouble(message.Data.GetValueOrDefault("value", 0));
            
            var metric = new MetricData
            {
                MetricName = metricName,
                Value = value,
                Timestamp = DateTime.UtcNow,
                Source = message.FromNodeId
            };
            
            StoreMetric(metric);
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Metrik speichern fehlgeschlagen");
            return false;
        }
    }
    
    private async Task<bool> HandleGetMetrics(NetworkMessage message)
    {
        var metricName = message.Data.GetValueOrDefault("metricName", "").ToString();
        
        List<MetricData> metrics;
        lock (_metricsLock)
        {
            if (string.IsNullOrEmpty(metricName))
            {
                metrics = _metricsHistory.Values.SelectMany(m => m).ToList();
            }
            else if (_metricsHistory.ContainsKey(metricName))
            {
                metrics = _metricsHistory[metricName];
            }
            else
            {
                metrics = new List<MetricData>();
            }
        }
        
        OnComponentEvent?.Invoke(this, new ComponentEventArgs
        {
            ComponentId = ComponentId,
            EventType = "MetricsRetrieved",
            Data = new Dictionary<string, object>
            {
                { "Metrics", metrics },
                { "Count", metrics.Count },
                { "RequestId", message.Id }
            }
        });
        
        return true;
    }
    
    private async Task<bool> HandleGetMetricsHistory(NetworkMessage message)
    {
        var hours = Convert.ToInt32(message.Data.GetValueOrDefault("hours", 1));
        var cutoff = DateTime.UtcNow.AddHours(-hours);
        
        var historyData = new Dictionary<string, object>();
        lock (_metricsLock)
        {
            foreach (var kvp in _metricsHistory)
            {
                var recentMetrics = kvp.Value.Where(m => m.Timestamp > cutoff).ToList();
                historyData[kvp.Key] = new
                {
                    MetricName = kvp.Key,
                    Count = recentMetrics.Count,
                    LatestValue = recentMetrics.LastOrDefault()?.Value,
                    AverageValue = recentMetrics.DefaultIfEmpty().Average(m => m?.Value ?? 0),
                    MinValue = recentMetrics.DefaultIfEmpty().Min(m => m?.Value ?? 0),
                    MaxValue = recentMetrics.DefaultIfEmpty().Max(m => m?.Value ?? 0)
                };
            }
        }
        
        OnComponentEvent?.Invoke(this, new ComponentEventArgs
        {
            ComponentId = ComponentId,
            EventType = "MetricsHistoryRetrieved",
            Data = new Dictionary<string, object>
            {
                { "History", historyData },
                { "Hours", hours },
                { "RequestId", message.Id }
            }
        });
        
        return true;
    }
    
    public async Task<NetworkMessage> CreateStatusMessage()
    {
        return new NetworkMessage
        {
            ComponentType = ComponentType,
            MessageType = "ComponentStatus",
            Data = GetStatus()
        };
    }
    
    public Dictionary<string, object> GetStatus()
    {
        lock (_metricsLock)
        {
            var totalMetrics = _metricsHistory.Values.Sum(m => m.Count);
            var metricTypes = _metricsHistory.Keys.Count;
            
            return new Dictionary<string, object>
            {
                { "ComponentId", ComponentId },
                { "Status", Status.ToString() },
                { "TotalMetrics", totalMetrics },
                { "MetricTypes", metricTypes },
                { "CollectionActive", Status == ComponentStatus.Running },
                { "AvailableMetrics", _metricsHistory.Keys.ToList() },
                { "Capabilities", new[] { "MetricsCollection", "MetricsStorage", "MetricsRetrieval", "HistoryAnalysis" } }
            };
        }
    }
    
    public async Task Shutdown()
    {
        Status = ComponentStatus.Stopped;
        _logger.LogInformation("🛑 Metrics Collector Netzwerk-Komponente heruntergefahren");
    }
}