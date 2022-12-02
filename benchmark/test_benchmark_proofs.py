from pypairing import ZR, G1, G2, pair, blsmultiexp
from adkg.extra_proofs import CP

import asyncio

def test_benchmark_pair(test_router, benchmark):
    loop = asyncio.get_event_loop()
    def _prog():
        loop.run_until_complete(run_pair())
    benchmark(_prog)

async def run_pair():
    g1, g2 = G1.rand(b'g'), G2.rand(b'g')
    alpha = ZR.rand()
    assert pair(g1**alpha, g2) == pair(g1, g2**alpha)

def test_benchmark_dleq(test_router, benchmark):
    loop = asyncio.get_event_loop()
    def _prog():
        loop.run_until_complete(run_dleq())
    benchmark(_prog)

async def run_dleq():
    g, h = G1.rand(b'g'), G1.rand(b'h')
    alpha = ZR.rand()
    cp = CP(g, h, ZR, blsmultiexp)
    x = g**alpha
    y = h**alpha
    pf = cp.prove(alpha, x, y)
    assert cp.verify(x, y, pf)