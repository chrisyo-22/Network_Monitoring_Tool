
export class NetworkPacket {
    constructor(packet_interface, destination, source, protocol, ipv4Packet, udpSegment, icmpPacket) {
        this.packet_interface = packet_interface;
        this.destination = destination;
        this.source = source;
        this.protocol = protocol;
        this.ipv4Packet = ipv4Packet;
        this.udpSegment = udpSegment;
        this.icmpPacket = icmpPacket;
    };
}