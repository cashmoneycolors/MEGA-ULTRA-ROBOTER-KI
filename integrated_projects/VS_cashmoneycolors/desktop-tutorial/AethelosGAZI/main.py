import asyncio
from core.echo import Echo
from agents.oracle import Oracle
from meta.gazi import GAZI

async def main():
    echo = Echo()
    oracle = Oracle(echo)
    gazi = GAZI(oracle)

    for _ in range(20):
        status = echo.get_instantaneous_status()
        decision = oracle.anticipate()
        print(f"Echo: {status} | Oracle: {decision}")
        if decision["intervention"]:
            print(">>> Oracle: Prädiktive Intervention ausgelöst!")
            gazi.audit_and_optimize()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
