import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge

def pack_inputs(a, b):
    # ui_in[3:0] = a, ui_in[7:4] = b
    return (b & 0xF) << 4 | (a & 0xF)

@cocotb.test()
async def adds_correctly(dut):
    """Tjekker at SUM = A + B på uo_out[4:0] for flere testvektorer."""
    # Start en "ligegyldig" clock (praktisk i cocotb, selv om designet er kombi)
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Sæt enable/reset i fornuftig tilstand
    dut.ena.value   = 1
    dut.rst_n.value = 1

    # Nogle håndplukkede testvektorer, inkl. carry
    vectors = [
        (0x0, 0x0),
        (0x1, 0x2),
        (0x3, 0x4),
        (0x7, 0x8),
        (0xA, 0x5),  # 10 + 5 = 15 (0xF)
        (0xF, 0x1),  # 15 + 1 = 16 (0b10000) -> carry bit
        (0xF, 0xF),  # 15 + 15 = 30 (0b11110)
    ]

    for a, b in vectors:
        dut.ui_in.value = pack_inputs(a, b)
        # Vent et par ns/clock-kanter for at give tid til kombinatorik
        await Timer(1, units="ns")
        await RisingEdge(dut.clk)

        expected = (a & 0xF) + (b & 0xF)     # 0..30
        got = int(dut.uo_out.value) & 0x1F   # kun [4:0]

        assert got == expected, f"Fejl for A={a} B={b}: forventede {expected}, fik {got}"
