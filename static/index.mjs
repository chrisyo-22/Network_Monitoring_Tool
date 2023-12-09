
import { NetworkPacket } from "./model/packetType.mjs";
import { getPacket } from "./api.mjs";

document.addEventListener('DOMContentLoaded', function () {
    const mockData = [
        { image: 'Discord.exe', pid: 16704, send: 207071, receive: 4209 },
        { image: 'SearchApp.exe', pid: 10348, send: 82978, receive: 7796 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604 },

        // ... add more mock data as needed
    ];


    const mockDataWithAdress = [
        { image: 'Discord.exe', pid: 16704, send: 207071, receive: 4209, address: '192.168.1.1' },
        { image: 'SearchApp.exe', pid: 10348, send: 82978, receive: 7796, address: '192.168.1.2' },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604, address: '192.168.1.3' },
        { image: 'SearchApp.exe', pid: 10348, send: 82978, receive: 7796, address: '192.168.1.2' },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604, address: '192.168.1.3' },
        { image: 'SearchApp.exe', pid: 10348, send: 82978, receive: 7796, address: '192.168.1.2' },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604, address: '192.168.1.3' },
        { image: 'SearchApp.exe', pid: 10348, send: 82978, receive: 7796, address: '192.168.1.2' },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604, address: '192.168.1.3' },
        { image: 'SearchApp.exe', pid: 10348, send: 82978, receive: 7796, address: '192.168.1.2' },
        { image: 'svchost.exe', pid: 5932, send: 0, receive: 1604, address: '192.168.1.3' },
        // ... more data
    ];

    
    const mockDataWithTCPConnections = [
        { image: 'Photoshop.exe', pid: 33869, LocalAddress: '6.180.100.177', LocalPort: '11449', RemoteAddress: '71.197.210.25', RemotePort: '51374', PacketLoss: '55%', Latency: '40ms' },
        { image: 'Slack.exe', pid: 32319, LocalAddress: '40.157.189.34', LocalPort: '41031', RemoteAddress: '23.28.214.110', RemotePort: '34607', PacketLoss: '51%', Latency: '47ms' },
        { image: 'Outlook.exe', pid: 15061, LocalAddress: '32.169.62.151', LocalPort: '57267', RemoteAddress: '252.242.68.169', RemotePort: '42384', PacketLoss: '5%', Latency: '83ms' },
        { image: 'Code.exe', pid: 41699, LocalAddress: '101.242.226.177', LocalPort: '3739', RemoteAddress: '92.191.39.21', RemotePort: '12589', PacketLoss: '75%', Latency: '66ms' },
        { image: 'Outlook.exe', pid: 12822, LocalAddress: '7.131.105.174', LocalPort: '26266', RemoteAddress: '84.189.211.94', RemotePort: '33756', PacketLoss: '95%', Latency: '49ms' },
        { image: 'Outlook.exe', pid: 12410, LocalAddress: '52.65.58.239', LocalPort: '34498', RemoteAddress: '179.34.150.6', RemotePort: '21395', PacketLoss: '28%', Latency: '45ms' },
        { image: 'Chrome.exe', pid: 46387, LocalAddress: '156.27.70.235', LocalPort: '5045', RemoteAddress: '149.145.191.154', RemotePort: '19882', PacketLoss: '61%', Latency: '83ms' }
    ];
    



    const process_toggle_btn = document.getElementById('toggle-process-activities-btn');
    const network_toggle_btn = document.getElementById('toggle-network-activities-btn');
    const tcp_connection_toggle_btn = document.getElementById('toggle-tcp-connection-btn');
    const listening_port_toggle_btn = document.getElementById('toggle-listening-port-btn');

    function updateProcessActivity(data) {
        const table = document.getElementById('process-activity-body');
        if (!table) {
            console.error('Could not find element with id "network-activity-body".');
            return;
        }

        if (!Array.isArray(data)) {
            console.error('Data is not an array.');
            return;
        }

        const tableBody = table.getElementsByTagName('tbody')[0] || document.createElement('tbody');
        table.appendChild(tableBody);
        tableBody.innerHTML = ''; // Clear existing table body

        data.forEach((process) => {
            if (!process || typeof process !== 'object' || !('image' in process) || !('pid' in process) || !('send' in process) || !('receive' in process)) {
                console.error('Invalid process data:', process);
                return;
            }

            const row = tableBody.insertRow();
            row.innerHTML = `
                <td>${process.image}</td>
                <td>${process.pid}</td>
                <td>${process.send}</td>
                <td>${process.receive}</td>
                <td>${process.send + process.receive}</td>
            `;
        });
    }


    function updateNetworkActivitity(data) {
        const table = document.getElementById('network-activity-body');
        if (!table) {
            console.error('Could not find element with id "network-activity-body".');
            return;
        }

        if (!Array.isArray(data)) {
            console.error('Data is not an array.');
            return;
        }

        const tableBody = table.getElementsByTagName('tbody')[0] || document.createElement('tbody');
        table.appendChild(tableBody);
        tableBody.innerHTML = ''; // Clear existing table body

        data.forEach((process) => {
            if (!process || typeof process !== 'object' || !('image' in process) || !('pid' in process) || !('send' in process) || !('receive' in process)) {
                console.error('Invalid process data:', process);
                return;
            }

            const row = tableBody.insertRow();
            row.innerHTML = `
                <td>${process.image}</td>
                <td>${process.pid}</td>
                <td>${process.address}</td>
                <td>${process.send}</td>
                <td>${process.receive}</td>
                <td>${process.send + process.receive}</td>
            `;
        });
    }

    function updateTCPConnections(data) {
        const table = document.getElementById('tcp-connection-body');
        if (!table) {
            console.error('Could not find element with id "network-activity-body".');
            return;
        }

        if (!Array.isArray(data)) {
            console.error('Data is not an array.');
            return;
        }

        const tableBody = table.getElementsByTagName('tbody')[0] || document.createElement('tbody');
        table.appendChild(tableBody);
        tableBody.innerHTML = ''; // Clear existing table body

        data.forEach((process) => {
            if (!process || typeof process !== 'object' ) {
                console.error('Invalid process data:', process);
                console.log("hi");
                return;
            }

            const row = tableBody.insertRow();
            row.innerHTML = `
                <td>${process.image}</td>
                <td>${process.pid}</td>
                <td>${process.LocalAddress}</td>
                <td>${process.LocalPort}</td>
                <td>${process.RemoteAddress}</td>
                <td>${process.RemotePort}</td>
                <td>${process.PacketLoss}</td>
                <td>${process.Latency}</td>
            `;
        });
    }
    function ListeningPorts(data) {
        const table = document.getElementById('listening-port-body');
        if (!table) {
            console.error('Could not find element with id "network-activity-body".');
            return;
        }

        if (!Array.isArray(data)) {
            console.error('Data is not an array.');
            return;
        }

        const tableBody = table.getElementsByTagName('tbody')[0] || document.createElement('tbody');
        table.appendChild(tableBody);
        tableBody.innerHTML = ''; // Clear existing table body

        data.forEach((process) => {
            if (!process || typeof process !== 'object' ) {
                console.error('Invalid process data:', process);
                console.log("hi");
                return;
            }

            const row = tableBody.insertRow();
            row.innerHTML = `
                <td>${process.image}</td>
                <td>${process.pid}</td>
                <td>${process.Address}</td>
                <td>${process.Port}</td>
                <td>${process.Protocol}</td>
                <td>${process.FirewallStatus}</td>
            `;
        });
    }


    function getListeningPortData(){
        const mockData = [
            { image: 'Chrome.exe', pid: 33555, Address: '227.35.70.146', Port: '56187', Protocol: 'UDP', FirewallStatus: 'Enabled' },
            { image: 'Code.exe', pid: 36951, Address: '66.90.225.53', Port: '36418', Protocol: 'UDP', FirewallStatus: 'Disabled' },
            { image: 'Outlook.exe', pid: 22206, Address: '94.236.101.165', Port: '34915', Protocol: 'UDP', FirewallStatus: 'Enabled' },
            { image: 'Chrome.exe', pid: 48856, Address: '97.92.170.58', Port: '53194', Protocol: 'UDP', FirewallStatus: 'Not Configured' },
            { image: 'Chrome.exe', pid: 19567, Address: '151.233.118.48', Port: '29980', Protocol: 'UDP', FirewallStatus: 'Not Configured' },
            { image: 'Slack.exe', pid: 17473, Address: '219.221.193.250', Port: '42445', Protocol: 'TCP', FirewallStatus: 'Enabled' },
            { image: 'Photoshop.exe', pid: 3899, Address: '2.44.231.229', Port: '60494', Protocol: 'TCP', FirewallStatus: 'Enabled' }
        ];
        return mockData;
    }

    function updateNetworkUtilization() {
        //call api to get data
        const network_IO = "232kb";
        const network_utilization = "23%";
        network_toggle_btn.innerHTML = `Network Activities:          Network IO: ${network_IO} | Network Utilization: ${network_utilization}`;

    }

    function addNewPacket(){
        //get newest packet
        /*
        *
        const packetData = await getPacket();
        if (packetData) {
        const packet = new NetworkPacket(
            packetData.interface, // Replace with actual keys from packetData
            packetData.destination,
            packetData.source,
            packetData.protocol,
            // ... Other parameters based on packetData structure
        );
        */
        const packet = new NetworkPacket(
            "lo",
            "00:00:00:00:00:00",
            "00:00:00:00:00:00",
            "8",
            { version: "4", headerLength: "20", ttl: "64", protocol: "17", source: "127.0.0.1", target: "127.0.0.53" },
            null,  // Assuming no UDP segment
            { type: "0", code: "0", checksum: "11805", data: "ICMP data..." }
        );
        console.log(packet)
        const container = document.getElementById('packet_container');

        let icmpDetails = '';
        if (packet.icmpPacket) {
            icmpDetails = `
                <p><strong>ICMP Type:</strong> ${packet.icmpPacket.type}</p>
                <p><strong>ICMP Code:</strong> ${packet.icmpPacket.code}</p>
                <p><strong>ICMP Checksum:</strong> ${packet.icmpPacket.checksum}</p>
                <p><strong>ICMP Data:</strong> ${packet.icmpPacket.data}</p>
            `;
        }
    
        let udpDetails = '';
        if (packet.udpSegment) {
            udpDetails = `
                <p><strong>UDP Source Port:</strong> ${packet.udpSegment.sourcePort}</p>
                <p><strong>UDP Destination Port:</strong> ${packet.udpSegment.destinationPort}</p>
                <p><strong>UDP Length:</strong> ${packet.udpSegment.length}</p>
                <p><strong>UDP Checksum:</strong> ${packet.udpSegment.checksum}</p>
            `;
        }
    
        const card = document.createElement('div');
        card.className = 'packet-card';
        card.innerHTML = `
            <div class="card-header">Packet ${packet.protocol}</div>
            <div class="card-body">
                <p><strong>Interface:</strong> ${packet.packet_interface}</p>
                <p><strong>Destination:</strong> ${packet.destination}</p>
                <p><strong>Source:</strong> ${packet.source}</p>
                <p><strong>Protocol:</strong> ${packet.ipv4Packet.protocol}</p>
                <p><strong>Version:</strong> ${packet.ipv4Packet.version}</p>
                <p><strong>Header Length:</strong> ${packet.ipv4Packet.headerLength}</p>
                <p><strong>TTL:</strong> ${packet.ipv4Packet.ttl}</p>
                <p><strong>IPv4 Source:</strong> ${packet.ipv4Packet.source}</p>
                <p><strong>IPv4 Target:</strong> ${packet.ipv4Packet.target}</p>
                ${icmpDetails}
                ${udpDetails}
            </div>
        `;
    
        container.appendChild(card);
    

        scrollToBottom(container);
    }

    function scrollToBottom(element) {
        element.scrollTop = element.scrollHeight;
    }


    process_toggle_btn.addEventListener('click', function () {
        const table = document.getElementById('process-activity-body');
        if (table.style.display === 'none') {
            table.style.display = '';
        } else {
            table.style.display = 'none';
        }
    });

    network_toggle_btn.addEventListener('click', function () {
        const table = document.getElementById('network-activity-body');
        if (table.style.display === 'none') {
            table.style.display = '';
        } else {
            table.style.display = 'none';
        }
    });

    tcp_connection_toggle_btn.addEventListener('click', function () {
        const table = document.getElementById('tcp-connection-body');
        if (table.style.display === 'none') {
            table.style.display = '';
        } else {
            table.style.display = 'none';
        }
    });

    listening_port_toggle_btn.addEventListener('click', function () {
        const table = document.getElementById('listening-port-body');
        if (table.style.display === 'none') {
            table.style.display = '';
        } else {
            table.style.display = 'none';
        }
    });

    // Initial update
    updateProcessActivity(mockData);
    updateNetworkActivitity(mockDataWithAdress);
    updateTCPConnections(mockDataWithTCPConnections);
    ListeningPorts(getListeningPortData());

    // Set interval to simulate real-time data update
    setInterval(() => {
        // Here you could simulate data changes
        updateProcessActivity(mockData);
        updateNetworkActivitity(mockDataWithAdress);
        updateTCPConnections(mockDataWithTCPConnections);
        ListeningPorts(getListeningPortData());
        updateNetworkUtilization();
        addNewPacket();
    }, 5000); // Update every 5 seconds
});
