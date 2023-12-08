
// static/script.js

document.addEventListener('DOMContentLoaded', function() {
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

    function updateNetworkActivityTable(data) {
        const tableBody = document.getElementById('network-activity-table').getElementsByTagName('tbody')[0] || document.createElement('tbody');
        document.getElementById('network-activity-table').appendChild(tableBody);
        tableBody.innerHTML = ''; // Clear existing table body

        data.forEach((process) => {
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

    function updateNetworkActivityGraph() {
        // This function would be responsible for updating the graph
        // For now, it's a placeholder
    }

    // Initial update
    updateNetworkActivityTable(mockData);
    updateNetworkActivityGraph();

    // Set interval to simulate real-time data update
    setInterval(() => {
        // Here you could simulate data changes
        updateNetworkActivityTable(mockData);
        updateNetworkActivityGraph();
    }, 5000); // Update every 5 seconds
});
