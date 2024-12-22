import asyncio
import os
from bot import Bot
from database.database import get_expired_files, remove_file_record

async def cleanup_expired_files():
    while True:
        try:
            expired_files = await get_expired_files()
            for file_entry in expired_files:
                try:
                    # Remove file record
                    await remove_file_record(file_entry['_id'])
                    
                    # Optional: Delete physical file
                    file_path = file_entry.get('file_path')
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Error processing expired file: {e}")
            
            await asyncio.sleep(3600)  # Check every hour
        except Exception as e:
            print(f"Cleanup error: {e}")
            await asyncio.sleep(3600)

class BotWithCleanup(Bot):
    async def start(self):
        # Start cleanup task only if it doesn't exist
        if not hasattr(self, 'cleanup_task'):
            self.cleanup_task = asyncio.create_task(cleanup_expired_files())
        await super().start()

    async def stop(self, *args):
        # Cancel cleanup task if it exists
        if hasattr(self, 'cleanup_task'):
            self.cleanup_task.cancel()
        await super().stop()

# Replace existing run with:
BotWithCleanup().run()
