import asyncio
import httpx
import uuid

BASE_URL = "http://localhost:8000"
session_id = str(uuid.uuid4())

async def main():
    print("Arty CLI - 'çıkış' yaz kapatmak için\n")
    
    async with httpx.AsyncClient(timeout=60) as client:
        while True:
            try:
                user_input = input("Sen: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGörüşürüz.")
                break
            
            if not user_input:
                continue
            if user_input.lower() in ["çıkış", "exit", "quit"]:
                print("Arty: Görüşürüz.")
                break
            
            response = await client.post(
                f"{BASE_URL}/chat",
                json={"message": user_input, "session_id": session_id}
            )
            data = response.json()
            print(f"Arty [{data['model'].split('/')[0]}]: {data['message']}\n")

if __name__ == "__main__":
    asyncio.run(main())
