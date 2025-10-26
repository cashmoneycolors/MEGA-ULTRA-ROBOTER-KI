using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Net.Http;
using System.Text.Json;
using System.Text;
using System.Linq;
using System.Net.Sockets;
using System.Net;
using System.Threading;
using System.Diagnostics;
using System.IO;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

using MegaUltra.Networking;

/// <summary>
/// 🌐 MEGA ULTRA NETWORK ORCHESTRATOR - KOMPLETTE VERNETZUNG 🌐
/// HYPER-VERNETZTES KI-ÖKOSYSTEM MIT MAXIMALER INTEGRATION
/// Alle Komponenten sind miteinander verbunden und kommunizieren in Echtzeit
/// Erstellt: 03. Oktober 2025 - Maximale Vernetzung implementiert
/// </summary>
public class MegaUltraNetworkOrchestrator : IDisposable
{
    // ===============================
    // 🌐 NETZWERK-KONFIGURATION
    // ===============================
    private readonly NetworkConfig _config;
    private readonly ILogger<MegaUltraNetworkOrchestrator> _logger;
    private readonly HttpClient _httpClient;
    
    // Netzwerk-Komponenten
    private readonly List<NetworkNode> _connectedNodes = new List<NetworkNode>();
    private readonly Dictionary<string, INetworkComponent> _components = new Dictionary<string, INetworkComponent>();
    private readonly CancellationTokenSource _networkCts = new CancellationTokenSource();
    
    // Kommunikations-Hubs
    private TcpListener _meshListener;
    private readonly Dictionary<string, TcpClient> _peerConnections = new Dictionary<string, TcpClient>();
    private readonly Queue<NetworkMessage> _messageQueue = new Queue<NetworkMessage>();
    
    // Event-System für Netzwerk-Kommunikation
    public event EventHandler<NetworkEventArgs> OnNetworkEvent;
    public event EventHandler<ComponentStatusArgs> OnComponentStatusChanged;
    public event EventHandler<DataSyncArgs> OnDataSynchronization;
    
    public class NetworkConfig
    {
        public string NodeId { get; set; } = Environment.MachineName + "_" + Guid.NewGuid().ToString("N")[..8];
        public int MeshPort { get; set; } = 4000;
        public int DiscoveryPort { get; set; } = 4001;
        public int SyncPort { get; set; } = 4002;
        public List<string> KnownPeers { get; set; } = new List<string>();
        public bool EnableAutoDiscovery { get; set; } = true;
        public bool EnableMeshNetworking { get; set; } = true;
        public bool EnableRealTimeSync { get; set; } = true;
        public TimeSpan HeartbeatInterval { get; set; } = TimeSpan.FromSeconds(5);
        public TimeSpan SyncInterval { get; set; } = TimeSpan.FromSeconds(10);
    }
    
    // ===============================
    // 🔗 NETZWERK-NACHRICHTEN-SYSTEM
    // ===============================
    // (Die Netzwerktypen sind jetzt ausschließlich im Namespace MegaUltra.Networking am Dateiende definiert)
    // ...
    // ===============================
    // 🚀 KONSTRUKTOR UND INITIALISIERUNG
    // ===============================
    public MegaUltraNetworkOrchestrator(NetworkConfig config = null, ILogger<MegaUltraNetworkOrchestrator> logger = null)
    {
        _config = config ?? new NetworkConfig();
        _logger = logger ?? CreateDefaultLogger();
        _httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(10) };
        
        _logger.LogInformation("🌐 MEGA ULTRA NETWORK ORCHESTRATOR INITIALISIERT");
        _logger.LogInformation($"📡 Node ID: {_config.NodeId}");
        _logger.LogInformation($"🔗 Mesh Port: {_config.MeshPort}");
        _logger.LogInformation($"🔍 Auto-Discovery: {(_config.EnableAutoDiscovery ? "✅" : "❌")}");
    }
    
    private ILogger<MegaUltraNetworkOrchestrator> CreateDefaultLogger()
    {
        var services = new ServiceCollection();
        services.AddLogging(builder => builder.AddConsole());
        var provider = services.BuildServiceProvider();
        return provider.GetRequiredService<ILogger<MegaUltraNetworkOrchestrator>>();
    }
    
    // ===============================
    // 🌐 NETZWERK-INITIALISIERUNG
    // ===============================
    public async Task InitializeNetwork()
    {
        try
        {
            _logger.LogInformation("🚀 Initialisiere Hyper-Vernetztes System...");
            
            // 1. Mesh-Netzwerk starten
            if (_config.EnableMeshNetworking)
            {
                await StartMeshNetwork();
            }
            
            // 2. Auto-Discovery starten
            if (_config.EnableAutoDiscovery)
            {
                _ = Task.Run(() => StartAutoDiscovery(_networkCts.Token));
            }
            
            // 3. Alle Komponenten registrieren und vernetzen
            await RegisterAllComponents();
            
            // 4. Heartbeat-System starten
            _ = Task.Run(() => StartHeartbeatSystem(_networkCts.Token));
            
            // 5. Message-Verarbeitung starten
            _ = Task.Run(() => ProcessMessageQueue(_networkCts.Token));
            
            // 6. Daten-Synchronisation starten
            if (_config.EnableRealTimeSync)
            {
                _ = Task.Run(() => StartDataSync(_networkCts.Token));
            }
            
            // 7. Bekannte Peers verbinden
            await ConnectToKnownPeers();
            
            _logger.LogInformation("✅ Hyper-Vernetztes System erfolgreich initialisiert!");
            
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "❌ Netzwerk-Initialisierung fehlgeschlagen");
            throw;
        }
    }
    
    // ===============================
    // 🔗 MESH-NETZWERK
    // ===============================
    private async Task StartMeshNetwork()
    {
        try
        {
            _meshListener = new TcpListener(IPAddress.Any, _config.MeshPort);
            _meshListener.Start();
            
            _logger.LogInformation($"🔗 Mesh-Netzwerk gestartet auf Port {_config.MeshPort}");
            
            // Akzeptiere eingehende Verbindungen
            _ = Task.Run(async () =>
            {
                while (!_networkCts.Token.IsCancellationRequested)
                {
                    try
                    {
                        var client = await _meshListener.AcceptTcpClientAsync();
                        _ = Task.Run(() => HandleIncomingConnection(client));
                    }
                    catch (ObjectDisposedException) { break; }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, "Fehler beim Akzeptieren einer Verbindung");
                    }
                }
            });
            
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Mesh-Netzwerk Start fehlgeschlagen");
            throw;
        }
    }
    
    private async Task HandleIncomingConnection(TcpClient client)
    {
        var remoteEndpoint = client.Client.RemoteEndPoint?.ToString() ?? "unknown";
        _logger.LogInformation($"🔗 Neue eingehende Verbindung von {remoteEndpoint}");
        
        try
        {
            var stream = client.GetStream();
            var buffer = new byte[4096];
            
            while (client.Connected && !_networkCts.Token.IsCancellationRequested)
            {
                var bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length);
                if (bytesRead == 0) break;
                
                var messageData = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                await ProcessIncomingMessage(messageData, remoteEndpoint);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Fehler bei Verbindung zu {remoteEndpoint}");
        }
        finally
        {
            client?.Close();
        }
    }
    
    private async Task ProcessIncomingMessage(string messageData, string sender)
    {
        try
        {
            var message = JsonSerializer.Deserialize<NetworkMessage>(messageData);
            if (message != null)
            {
                _logger.LogDebug($"📥 Nachricht empfangen von {sender}: {message.MessageType}");
                
                // Message in Queue einreihen
                lock (_messageQueue)
                {
                    _messageQueue.Enqueue(message);
                }
                
                // Event auslösen
                OnNetworkEvent?.Invoke(this, new NetworkEventArgs
                {
                    NodeId = sender,
                    EventType = "MessageReceived",
                    Message = message
                });
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Fehler beim Verarbeiten der Nachricht von {sender}");
        }
    }
    
    // ===============================
    // 🔍 AUTO-DISCOVERY SYSTEM
    // ===============================
    private async Task StartAutoDiscovery(CancellationToken token)
    {
        _logger.LogInformation("🔍 Auto-Discovery System gestartet");
        
        using var udpClient = new UdpClient(_config.DiscoveryPort);
        udpClient.EnableBroadcast = true;
        
        // Discovery-Broadcasts senden
        _ = Task.Run(async () =>
        {
            while (!token.IsCancellationRequested)
            {
                try
                {
                    var discoveryMessage = new
                    {
                        NodeId = _config.NodeId,
                        MeshPort = _config.MeshPort,
                        Timestamp = DateTime.UtcNow,
                        Capabilities = GetNodeCapabilities()
                    };
                    
                    var messageBytes = Encoding.UTF8.GetBytes(JsonSerializer.Serialize(discoveryMessage));
                    var broadcastEndpoint = new IPEndPoint(IPAddress.Broadcast, _config.DiscoveryPort);
                    
                    await udpClient.SendAsync(messageBytes, messageBytes.Length, broadcastEndpoint);
                    
                    await Task.Delay(TimeSpan.FromSeconds(30), token);
                }
                catch (Exception ex) when (!(ex is OperationCanceledException))
                {
                    _logger.LogError(ex, "Discovery-Broadcast Fehler");
                    await Task.Delay(TimeSpan.FromSeconds(60), token);
                }
            }
        });
        
        // Discovery-Nachrichten empfangen
        while (!token.IsCancellationRequested)
        {
            try
            {
                var result = await udpClient.ReceiveAsync();
                var messageData = Encoding.UTF8.GetString(result.Buffer);
                
                await ProcessDiscoveryMessage(messageData, result.RemoteEndPoint.Address.ToString());
            }
            catch (Exception ex) when (!(ex is OperationCanceledException))
            {
                _logger.LogError(ex, "Discovery-Empfang Fehler");
                await Task.Delay(TimeSpan.FromSeconds(5), token);
            }
        }
    }
    
    private async Task ProcessDiscoveryMessage(string messageData, string senderIP)
    {
        try
        {
            var discoveryData = JsonSerializer.Deserialize<JsonElement>(messageData);
            
            if (discoveryData.TryGetProperty("NodeId", out var nodeIdElement))
            {
                var nodeId = nodeIdElement.GetString();
                
                // Ignore eigene Broadcasts
                if (nodeId == _config.NodeId) return;
                
                var meshPort = discoveryData.GetProperty("MeshPort").GetInt32();
                
                // Neuen Node hinzufügen oder aktualisieren
                var existingNode = _connectedNodes.FirstOrDefault(n => n.NodeId == nodeId);
                if (existingNode == null)
                {
                    var newNode = new NetworkNode
                    {
                        NodeId = nodeId,
                        IPAddress = senderIP,
                        Port = meshPort,
                        LastSeen = DateTime.UtcNow,
                        Status = NodeStatus.Connecting
                    };
                    
                    if (discoveryData.TryGetProperty("Capabilities", out var capabilitiesElement))
                    {
                        newNode.Capabilities = JsonSerializer.Deserialize<Dictionary<string, object>>(capabilitiesElement.GetRawText());
                    }
                    
                    _connectedNodes.Add(newNode);
                    _logger.LogInformation($"🔍 Neuen Node entdeckt: {nodeId} @ {senderIP}:{meshPort}");
                    
                    // Versuche Verbindung aufzubauen
                    _ = Task.Run(() => ConnectToPeer(newNode));
                }
                else
                {
                    existingNode.LastSeen = DateTime.UtcNow;
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Discovery-Message Verarbeitung fehlgeschlagen");
        }
    }
    
    private Dictionary<string, object> GetNodeCapabilities()
    {
        return new Dictionary<string, object>
        {
            { "Type", "MegaUltraNode" },
            { "Version", "2.0.0" },
            { "Components", _components.Keys.ToList() },
            { "MaxConnections", 100 },
            { "SupportedProtocols", new[] { "HTTP", "TCP", "UDP", "WebSocket" } },
            { "Features", new[] { "MeshNetworking", "AutoDiscovery", "RealTimeSync", "LoadBalancing" } }
        };
    }
    
    // ===============================
    // 🔗 PEER-VERBINDUNGEN
    // ===============================
    private async Task ConnectToPeer(NetworkNode node)
    {
        try
        {
            _logger.LogInformation($"🔗 Verbinde zu Peer {node.NodeId} @ {node.IPAddress}:{node.Port}");
            
            var client = new TcpClient();
            await client.ConnectAsync(IPAddress.Parse(node.IPAddress), node.Port);
            
            lock (_peerConnections)
            {
                _peerConnections[node.NodeId] = client;
            }
            
            node.Status = NodeStatus.Connected;
            node.LastSeen = DateTime.UtcNow;
            
            _logger.LogInformation($"✅ Verbindung zu {node.NodeId} hergestellt");
            
            // Handshake-Nachricht senden
            await SendMessage(new NetworkMessage
            {
                ToNodeId = node.NodeId,
                FromNodeId = _config.NodeId,
                MessageType = "Handshake",
                Data = new Dictionary<string, object>
                {
                    { "Capabilities", GetNodeCapabilities() },
                    { "Timestamp", DateTime.UtcNow }
                }
            });
            
            // Verbindung überwachen
            _ = Task.Run(() => MonitorPeerConnection(node, client));
            
        }
        catch (Exception ex)
        {
            node.Status = NodeStatus.Error;
            _logger.LogError(ex, $"Verbindung zu {node.NodeId} fehlgeschlagen");
        }
    }
    
    private async Task ConnectToKnownPeers()
    {
        foreach (var peerAddress in _config.KnownPeers)
        {
            try
            {
                var parts = peerAddress.Split(':');
                if (parts.Length == 2 && int.TryParse(parts[1], out var port))
                {
                    var node = new NetworkNode
                    {
                        NodeId = $"KnownPeer_{peerAddress}",
                        IPAddress = parts[0],
                        Port = port,
                        Status = NodeStatus.Connecting
                    };
                    
                    _connectedNodes.Add(node);
                    await ConnectToPeer(node);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Verbindung zu bekanntem Peer {peerAddress} fehlgeschlagen");
            }
        }
    }
    
    private async Task MonitorPeerConnection(NetworkNode node, TcpClient client)
    {
        while (client.Connected && !_networkCts.Token.IsCancellationRequested)
        {
            try
            {
                await Task.Delay(_config.HeartbeatInterval, _networkCts.Token);
                
                // Ping senden
                var startTime = DateTime.UtcNow;
                await SendMessage(new NetworkMessage
                {
                    ToNodeId = node.NodeId,
                    FromNodeId = _config.NodeId,
                    MessageType = "Ping",
                    RequiresResponse = true
                });
                
                // Latenz messen (vereinfacht)
                node.Latency = (DateTime.UtcNow - startTime).TotalMilliseconds;
                node.LastSeen = DateTime.UtcNow;
                
            }
            catch (Exception ex) when (!(ex is OperationCanceledException))
            {
                _logger.LogWarning($"Heartbeat zu {node.NodeId} fehlgeschlagen: {ex.Message}");
                break;
            }
        }
        
        // Verbindung bereinigen
        node.Status = NodeStatus.Disconnected;
        lock (_peerConnections)
        {
            _peerConnections.Remove(node.NodeId);
        }
        client?.Close();
        
        _logger.LogWarning($"🔗 Verbindung zu {node.NodeId} getrennt");
    }
    
    // ===============================
    // 📨 NACHRICHTEN-SYSTEM
    // ===============================
    public async Task SendMessage(NetworkMessage message)
    {
        try
        {
            var messageJson = JsonSerializer.Serialize(message);
            var messageBytes = Encoding.UTF8.GetBytes(messageJson);
            
            if (string.IsNullOrEmpty(message.ToNodeId))
            {
                // Broadcast an alle verbundenen Nodes
                await BroadcastMessage(messageBytes);
            }
            else
            {
                // Unicast an spezifischen Node
                await SendMessageToNode(message.ToNodeId, messageBytes);
            }
            
            _logger.LogDebug($"📤 Nachricht gesendet: {message.MessageType} -> {message.ToNodeId ?? "BROADCAST"}");
            
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Nachricht senden fehlgeschlagen: {message.MessageType}");
        }
    }
    
    private async Task BroadcastMessage(byte[] messageBytes)
    {
        var tasks = new List<Task>();
        
        lock (_peerConnections)
        {
            foreach (var kvp in _peerConnections)
            {
                tasks.Add(SendMessageToClient(kvp.Value, messageBytes, kvp.Key));
            }
        }
        
        await Task.WhenAll(tasks);
    }
    
    private async Task SendMessageToNode(string nodeId, byte[] messageBytes)
    {
        TcpClient client;
        lock (_peerConnections)
        {
            if (!_peerConnections.TryGetValue(nodeId, out client))
            {
                throw new InvalidOperationException($"Keine Verbindung zu Node {nodeId}");
            }
        }
        
        await SendMessageToClient(client, messageBytes, nodeId);
    }
    
    private async Task SendMessageToClient(TcpClient client, byte[] messageBytes, string nodeId)
    {
        try
        {
            if (client.Connected)
            {
                var stream = client.GetStream();
                await stream.WriteAsync(messageBytes, 0, messageBytes.Length);
                await stream.FlushAsync();
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Nachricht zu {nodeId} senden fehlgeschlagen");
        }
    }
    
    private async Task ProcessMessageQueue(CancellationToken token)
    {
        _logger.LogInformation("📨 Message-Queue-Processor gestartet");
        
        while (!token.IsCancellationRequested)
        {
            try
            {
                NetworkMessage message = null;
                lock (_messageQueue)
                {
                    if (_messageQueue.Count > 0)
                    {
                        message = _messageQueue.Dequeue();
                    }
                }
                
                if (message != null)
                {
                    await ProcessNetworkMessage(message);
                }
                else
                {
                    await Task.Delay(100, token);
                }
            }
            catch (Exception ex) when (!(ex is OperationCanceledException))
            {
                _logger.LogError(ex, "Message-Queue Verarbeitung fehlgeschlagen");
                await Task.Delay(1000, token);
            }
        }
    }
    
    private async Task ProcessNetworkMessage(NetworkMessage message)
    {
        try
        {
            _logger.LogDebug($"📥 Verarbeite Nachricht: {message.MessageType} von {message.FromNodeId}");
            
            switch (message.MessageType)
            {
                case "Handshake":
                    await HandleHandshakeMessage(message);
                    break;
                
                case "Ping":
                    if (message.RequiresResponse)
                    {
                        await SendMessage(new NetworkMessage
                        {
                            ToNodeId = message.FromNodeId,
                            FromNodeId = _config.NodeId,
                            MessageType = "Pong",
                            Data = new Dictionary<string, object>
                            {
                                { "OriginalId", message.Id },
                                { "Timestamp", DateTime.UtcNow }
                            }
                        });
                    }
                    break;
                
                case "ComponentStatus":
                    await HandleComponentStatusMessage(message);
                    break;
                
                case "DataSync":
                    await HandleDataSyncMessage(message);
                    break;
                
                case "LoadBalanceRequest":
                    await HandleLoadBalanceMessage(message);
                    break;
                
                default:
                    // An entsprechende Komponente weiterleiten
                    if (_components.TryGetValue(message.ComponentType, out var component))
                    {
                        await component.ProcessMessage(message);
                    }
                    break;
            }
            
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Nachricht-Verarbeitung fehlgeschlagen: {message.MessageType}");
        }
    }
    
    // ===============================
    // 🔧 KOMPONENTEN-REGISTRIERUNG
    // ===============================
    public void RegisterComponent(INetworkComponent component)
    {
        _components[component.ComponentId] = component;
        component.OnComponentEvent += HandleComponentEvent;
        
        _logger.LogInformation($"🔧 Komponente registriert: {component.ComponentId} ({component.ComponentType})");
        
        // Status-Broadcast an alle Nodes
        _ = Task.Run(async () =>
        {
            await SendMessage(new NetworkMessage
            {
                MessageType = "ComponentRegistered",
                ComponentType = component.ComponentType,
                Data = new Dictionary<string, object>
                {
                    { "ComponentId", component.ComponentId },
                    { "Status", component.Status.ToString() },
                    { "Capabilities", component.GetStatus() }
                }
            });
        });
    }
    
    private async Task RegisterAllComponents()
    {
        _logger.LogInformation("🔧 Registriere alle Netzwerk-Komponenten...");
        
        // AI Integrator Komponente
        var aiIntegrator = new AIIntegratorNetworkComponent();
    RegisterComponent(aiIntegrator);
    await aiIntegrator.Initialize();

    // GazOpenAIIntegrator Komponente
    var gazOpenAI = new GazOpenAIIntegrator();
    RegisterComponent(gazOpenAI);
    await gazOpenAI.Initialize();

    // Node.js Server Komponente
    var nodeServer = new NodeServerNetworkComponent();
    RegisterComponent(nodeServer);
    await nodeServer.Initialize();

    // Ollama LLM Komponente
    var ollamaLLM = new OllamaLLMNetworkComponent();
    RegisterComponent(ollamaLLM);
    await ollamaLLM.Initialize();

    // Database Komponente
    var database = new DatabaseNetworkComponent();
    RegisterComponent(database);
    await database.Initialize();

    // Security Monitor Komponente
    var securityMonitor = new SecurityMonitorNetworkComponent();
    RegisterComponent(securityMonitor);
    await securityMonitor.Initialize();

    // Load Balancer Komponente
    var loadBalancer = new LoadBalancerNetworkComponent(this);
    RegisterComponent(loadBalancer);
    await loadBalancer.Initialize();
        
        _logger.LogInformation($"✅ {_components.Count} Komponenten erfolgreich registriert und vernetzt");
    }
    
    private void HandleComponentEvent(object sender, ComponentEventArgs e)
    {
        _logger.LogInformation($"🔧 Komponenten-Event: {e.ComponentId} - {e.EventType}");
        
        // Event an alle Nodes weiterleiten
        _ = Task.Run(async () =>
        {
            await SendMessage(new NetworkMessage
            {
                MessageType = "ComponentEvent",
                ComponentType = ((INetworkComponent)sender).ComponentType,
                Data = new Dictionary<string, object>
                {
                    { "ComponentId", e.ComponentId },
                    { "EventType", e.EventType },
                    { "EventData", e.Data }
                }
            });
        });
        
        OnComponentStatusChanged?.Invoke(this, new ComponentStatusArgs
        {
            ComponentId = e.ComponentId
        });
    }
    
    // ===============================
    // 📊 DATEN-SYNCHRONISATION
    // ===============================
    private async Task StartDataSync(CancellationToken token)
    {
        _logger.LogInformation("📊 Daten-Synchronisation gestartet");
        
        while (!token.IsCancellationRequested)
        {
            try
            {
                await Task.Delay(_config.SyncInterval, token);
                await PerformDataSync();
            }
            catch (Exception ex) when (!(ex is OperationCanceledException))
            {
                _logger.LogError(ex, "Daten-Synchronisation fehlgeschlagen");
                await Task.Delay(TimeSpan.FromSeconds(30), token);
            }
        }
    }
    
    private async Task PerformDataSync()
    {
        try
        {
            var syncData = new Dictionary<string, object>();
            
            // Status aller Komponenten sammeln
            foreach (var component in _components.Values)
            {
                syncData[component.ComponentId] = component.GetStatus();
            }
            
            // Node-Informationen hinzufügen
            syncData["NetworkNodes"] = _connectedNodes.Select(n => new
            {
                n.NodeId,
                n.IPAddress,
                n.Port,
                n.Status,
                n.LastSeen,
                n.Latency
            }).ToList();
            
            // Sync-Nachricht an alle Nodes senden
            await SendMessage(new NetworkMessage
            {
                MessageType = "DataSync",
                Data = syncData,
                Priority = 1
            });
            
            _logger.LogDebug("📊 Daten-Synchronisation durchgeführt");
            
            OnDataSynchronization?.Invoke(this, new DataSyncArgs
            {
                DataType = "FullSync",
                SyncData = syncData,
                TargetNodes = _connectedNodes.Select(n => n.NodeId).ToList()
            });
            
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Daten-Synchronisation Fehler");
        }
    }
    
    // ===============================
    // 💓 HEARTBEAT-SYSTEM
    // ===============================
    private async Task StartHeartbeatSystem(CancellationToken token)
    {
        _logger.LogInformation("💓 Heartbeat-System gestartet");
        
        while (!token.IsCancellationRequested)
        {
            try
            {
                await Task.Delay(_config.HeartbeatInterval, token);
                await SendHeartbeat();
                await CheckNodeHealth();
            }
            catch (Exception ex) when (!(ex is OperationCanceledException))
            {
                _logger.LogError(ex, "Heartbeat-System Fehler");
                await Task.Delay(TimeSpan.FromSeconds(10), token);
            }
        }
    }
    
    private async Task SendHeartbeat()
    {
        await SendMessage(new NetworkMessage
        {
            MessageType = "Heartbeat",
            Data = new Dictionary<string, object>
            {
                { "NodeId", _config.NodeId },
                { "Timestamp", DateTime.UtcNow },
                { "ComponentCount", _components.Count },
                { "Status", "Running" }
            }
        });
    }
    
    private async Task CheckNodeHealth()
    {
        var now = DateTime.UtcNow;
        var timeoutThreshold = TimeSpan.FromSeconds(60);
        
        var deadNodes = _connectedNodes.Where(n => 
            now - n.LastSeen > timeoutThreshold && 
            n.Status == NodeStatus.Connected).ToList();
        
        foreach (var deadNode in deadNodes)
        {
            deadNode.Status = NodeStatus.Disconnected;
            _logger.LogWarning($"💀 Node {deadNode.NodeId} als tot markiert (letzter Kontakt: {deadNode.LastSeen})");
            
            // Verbindung bereinigen
            lock (_peerConnections)
            {
                if (_peerConnections.TryGetValue(deadNode.NodeId, out var client))
                {
                    client.Close();
                    _peerConnections.Remove(deadNode.NodeId);
                }
            }
        }
    }
    
    // ===============================
    // 📨 MESSAGE-HANDLER
    // ===============================
    private async Task HandleHandshakeMessage(NetworkMessage message)
    {
        _logger.LogInformation($"🤝 Handshake von {message.FromNodeId}");
        
        if (message.Data.TryGetValue("Capabilities", out var capabilitiesObj))
        {
            var capabilities = capabilitiesObj as Dictionary<string, object>;
            var node = _connectedNodes.FirstOrDefault(n => n.NodeId == message.FromNodeId);
            if (node != null)
            {
                node.Capabilities = capabilities ?? new Dictionary<string, object>();
            }
        }
        
        // Handshake-Response senden
        await SendMessage(new NetworkMessage
        {
            ToNodeId = message.FromNodeId,
            FromNodeId = _config.NodeId,
            MessageType = "HandshakeResponse",
            Data = new Dictionary<string, object>
            {
                { "Capabilities", GetNodeCapabilities() },
                { "AcceptedConnection", true }
            }
        });
    }
    
    private async Task HandleComponentStatusMessage(NetworkMessage message)
    {
        // Komponenten-Status von anderen Nodes verarbeiten
        _logger.LogDebug($"🔧 Komponenten-Status von {message.FromNodeId}");
        
        // Status-Informationen an lokale Komponenten weiterleiten
        foreach (var component in _components.Values)
        {
            await component.ProcessMessage(message);
        }
    }
    
    private async Task HandleDataSyncMessage(NetworkMessage message)
    {
        _logger.LogDebug($"📊 Daten-Sync von {message.FromNodeId}");
        
        // Sync-Daten verarbeiten und lokale Komponenten aktualisieren
        foreach (var kvp in message.Data)
        {
            if (_components.TryGetValue(kvp.Key, out var component))
            {
                await component.ProcessMessage(new NetworkMessage
                {
                    MessageType = "SyncUpdate",
                    Data = new Dictionary<string, object> { { "SyncData", kvp.Value } }
                });
            }
        }
    }
    
    private async Task HandleLoadBalanceMessage(NetworkMessage message)
    {
        if (_components.TryGetValue("LoadBalancer", out var loadBalancer))
        {
            await loadBalancer.ProcessMessage(message);
        }
    }
    
    // ===============================
    // 📊 NETZWERK-STATUS UND METRIKEN
    // ===============================
    public Dictionary<string, object> GetNetworkStatus()
    {
        return new Dictionary<string, object>
        {
            { "NodeId", _config.NodeId },
            { "ConnectedNodes", _connectedNodes.Count(n => n.Status == NodeStatus.Connected) },
            { "TotalNodes", _connectedNodes.Count },
            { "RegisteredComponents", _components.Count },
            { "NetworkHealth", CalculateNetworkHealth() },
            { "Nodes", _connectedNodes.Select(n => new
                {
                    n.NodeId,
                    n.IPAddress,
                    n.Status,
                    n.LastSeen,
                    n.Latency
                }).ToList() },
            { "Components", _components.Values.Select(c => new
                {
                    c.ComponentId,
                    c.ComponentType,
                    c.Status
                }).ToList() }
        };
    }
    
    private double CalculateNetworkHealth()
    {
        if (_connectedNodes.Count == 0) return 100.0;
        
        var connectedCount = _connectedNodes.Count(n => n.Status == NodeStatus.Connected);
        var healthyComponents = _components.Values.Count(c => c.Status == ComponentStatus.Running);
        
        var nodeHealth = (double)connectedCount / _connectedNodes.Count * 100;
        var componentHealth = _components.Count > 0 ? (double)healthyComponents / _components.Count * 100 : 100;
        
        return (nodeHealth + componentHealth) / 2;
    }
    
    // ===============================
    // 🗑️ BEREINIGUNG
    // ===============================
    public void Dispose()
    {
        _logger.LogInformation("🧹 Netzwerk-Orchestrator wird heruntergefahren...");
        
        _networkCts?.Cancel();
        
        // Shutdown-Nachricht an alle Nodes senden
        try
        {
            SendMessage(new NetworkMessage
            {
                MessageType = "NodeShutdown",
                Data = new Dictionary<string, object>
                {
                    { "NodeId", _config.NodeId },
                    { "Reason", "Graceful Shutdown" }
                }
            }).Wait(TimeSpan.FromSeconds(5));
        }
        catch { }
        
        // Alle Komponenten herunterfahren
        foreach (var component in _components.Values)
        {
            try
            {
                component.Shutdown().Wait(TimeSpan.FromSeconds(5));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Komponente {component.ComponentId} Shutdown-Fehler");
            }
        }
        
        // Netzwerk-Verbindungen schließen
        _meshListener?.Stop();
        
        lock (_peerConnections)
        {
            foreach (var client in _peerConnections.Values)
            {
                try { client.Close(); } catch { }
            }
            _peerConnections.Clear();
        }
        
        _httpClient?.Dispose();
        _networkCts?.Dispose();
        
        _logger.LogInformation("✅ Netzwerk-Orchestrator heruntergefahren");
    }
}

// ===============================
// 🔗 NETZWERK-TYPEN (für alle Komponenten)
// ===============================
namespace MegaUltra.Networking
{
    public class NetworkMessage
    {
        public string Id { get; set; } = Guid.NewGuid().ToString();
        public string FromNodeId { get; set; }
        public string ToNodeId { get; set; }
        public string ComponentType { get; set; }
        public string MessageType { get; set; }
        public Dictionary<string, object> Data { get; set; } = new Dictionary<string, object>();
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
        public int Priority { get; set; } = 0; // 0=Normal, 1=High, 2=Critical
        public bool RequiresResponse { get; set; } = false;
    }

    public class NetworkNode
    {
        public string NodeId { get; set; }
        public string IPAddress { get; set; }
        public int Port { get; set; }
        public DateTime LastSeen { get; set; }
        public Dictionary<string, object> Capabilities { get; set; } = new Dictionary<string, object>();
        public NodeStatus Status { get; set; } = NodeStatus.Unknown;
        public double Latency { get; set; }
    }

    public enum NodeStatus { Unknown, Connecting, Connected, Disconnected, Error }

    public interface INetworkComponent
    {
        string ComponentId { get; }
        string ComponentType { get; }
        ComponentStatus Status { get; }
        Dictionary<string, object> GetStatus();
        Task<bool> ProcessMessage(NetworkMessage message);
        Task<NetworkMessage> CreateStatusMessage();
        Task Initialize();
        Task Shutdown();
        event EventHandler<ComponentEventArgs> OnComponentEvent;
    }

    public enum ComponentStatus { Stopped, Starting, Running, Error, Maintenance }

    public class ComponentEventArgs : EventArgs
    {
        public string ComponentId { get; set; }
        public string EventType { get; set; }
        public Dictionary<string, object> Data { get; set; }
    }

    public class NetworkEventArgs : EventArgs
    {
        public string NodeId { get; set; }
        public string EventType { get; set; }
        public NetworkMessage Message { get; set; }
    }
    public class ComponentStatusArgs : EventArgs
    {
        public string ComponentId { get; set; }
        public ComponentStatus OldStatus { get; set; }
        public ComponentStatus NewStatus { get; set; }
    }

    public class DataSyncArgs : EventArgs
    {
        public string DataType { get; set; }
        public Dictionary<string, object> SyncData { get; set; }
        public List<string> TargetNodes { get; set; }
    }
}