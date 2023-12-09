export async function getPacket() {
    try {
        const response = await fetch('/packetSniff');
        const data = await response.json();
        return data; // Return the fetched data
    } catch (error) {
        console.error('Error:', error);
    }
}
