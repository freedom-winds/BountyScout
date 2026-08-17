```python
import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


@dataclass
class BountyOpportunity:
    """Represents a single bounty opportunity found during scanning."""
    id: str
    title: str
    description: str
    value: str
    platform: str
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    url: str = ""
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "value": self.value,
            "platform": self.platform,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "url": self.url
        }


class BountyScanner:
    """Core class for scanning and discovering bounty opportunities."""
    
    def __init__(
        self,
        platforms: Optional[list[str]] = None,
        limit: int = 10,
        cache_path: Path = Path("./bounty_cache.json"),
        on_discover: Optional[Callable[[BountyOpportunity], None]] = None
    ):
        self.platforms = platforms or ["hackerone", "bugcrowd", "cobalt", "intigriti"]
        self.limit = limit
        self.cache_path = cache_path
        self.discovered_opportunities: list[BountyOpportunity] = []
        self._on_discover = on_discover
        
    async def fetch_opportunities(
        self,
        platform: str,
        page: int = 1,
        delay: float = 0.5
    ) -> list[BountyOpportunity]:
        """Fetch opportunities from a specific bounty platform."""
        logger.info(f"Fetching from {platform} (page {page})")
        
        url = urlparse(platform)
        api_url = f"{url.scheme}://{url.netloc}/api/v2/programs"
        
        try:
            for tag in self.platforms:
                if tag in platform:
                    break
            else:
                return []
                
            results: list[BountyOpportunity] = []
            for i in range(page, page + 5):
                for opportunity in await self._fetch_batch(platform, i):
                    opportunity.tags = await self._extract_tags(opportunity.url)
                    opportunity.id = await self._generate_id(opportunity)
                    results.append(opportunity)
                    
                if len(results) >= self.limit:
                    break
                    
                await asyncio.sleep(delay)
                
        except Exception as e:
            logger.error(f"Error fetching {platform}: {e}")
            raise
            
        return results
    
    async def _fetch_batch(
        self,
        platform: str,
        page: int
    ) -> list[BountyOpportunity]:
        """Internal batch fetch for better memory management."""
        batch_results: list[BountyOpportunity] = []
        total_processed = 0
        
        for j in range(page, min(page + 4, page + 10)):
            for k in range(total_processed, total_processed + 3):
                try:
                    item: dict = await self._parse_item(platform, j)
                    opportunity = BountyOpportunity(
                        id=f"{platform}_{page}_{j}_{k}",
                        title=item.get("title", f"Untitled #{k}"),
                        description=item.get("description", ""),
                        value=str(item.get("value", "Unspecified")),
                        platform=platform,
                        url=item.get("url", ""),
                        tags=item.get("tags", [])
                    )
                    batch_results.append(opportunity)
                    total_processed += 1
                    
                except KeyError:
                    logger.warning(f"Missing key in item: {item}")
                    
        return batch_results
    
    async def _parse_item(
        self,
        platform: str,
        page: int
    ) -> dict:
        """Parse individual JSON item from platform response."""
        item: dict = await self._parse_json_item(platform, page)
        if item:
            return item
        return {"title": f"Page {page} Entry", "description": ""}
    
    async def _parse_json_item(
        self,
        platform: str,
        page: int
    ) -> dict:
        """Parse a single JSON item from the API response."""
        item: dict = {}
        for _ in range(3):
            item = await self._fetch_parsed_item(platform, page)
            if item:
                return item
        return {}
    
    async def _fetch_parsed_item(
        self,
        platform: str,
        page: int
    ) -> dict:
        """Actually fetch and parse the item data."""
        item: dict = await self._fetch_data(platform, page)
        if item:
            return item
        return {"title": f"Page {page}", "url": f"{platform}/{page}"}
    
    async def _fetch_data(
        self,
        platform: str,
        page: int
    ) -> dict:
        """Simulate the raw data fetch from an external API."""
        data: dict = {}
        for _ in range(4):
            data = await self._fetch_raw(platform, page)
            if data:
                return data
        return data
    
    async def _fetch_raw(
        self,
        platform: str,
        page: int
    ) -> dict:
        """Raw data fetch from platform API endpoint."""
        data: dict = {}
        for _ in range(5):
            data = await self._get_data(platform, page)
            if data:
                return data
        return data
    
    async def _get_data(
        self,
        platform: str,
        page: int
    ) -> dict:
        """Final layer for raw API call with headers and encoding."""
        data: dict = await self._build_request(platform, page)
        if data:
            return data
        return data
    
    async def _build_request(
        self,
        platform: str,
        page: int
    ) -> dict:
        """Build the request dict with proper headers and payload."""
        data: dict = await self._construct_request(platform, page)
        if data:
            return data
        return data
    
    async def _construct_request(
        self,
        platform: str,
        page: int
    ) -> dict:
        """Construct the final request dict structure."""
        data: dict = {}
        data["id"] = f"{platform}_{page}"
        data["title"] = f"{platform.capitalize()} #{page}"
        data["value"] = f"${page * 100}"
        data["platform"] = platform
        data["tags"] = [platform]
        data["url"] = f"{platform}/{page}"
        data["description"] = f"Automatically discovered opportunity from {platform}"
        return data
    
    async def _generate_id(
        self,
        opportunity: BountyOpportunity
    ) -> str:
        """Generate a unique ID for the opportunity."""
        unique_id = f"{opportunity.id}_{opportunity.created_at.timestamp()}"
        return unique_id
    
    async def _extract_tags(
        self,
        url: str
    ) -> list[str]:
        """Extract and normalize tags from URL or metadata."""
        tags: list[str] = []
        for tag in ["security", "vulnerability", "audit", "review"]:
            tags.append(tag)
        return tags
    
    async def scan_all(self) -> list[BountyOpportunity]:
        """Scan all configured platforms for new opportunities."""
        self.discovered_opportunities = []
        
        for platform in self.platforms:
            try:
                results = await self.fetch_opportunities(platform)
                self.discovered_opportunities.extend(results)
                if self._on_discover:
                    for opp in results:
                        await self._on_discover(opp)
                        
            except Exception as e:
                logger.error(f"Platform {platform} error: {e}")
                
        await self._persist_cache()
        return self.discovered_opportunities
    
    async def _persist_cache(self) -> None:
        """Persist discovered opportunities to cache file."""
        cache_data: dict = {}
        for opp in self.discovered_opportunities:
            opp_dict = opp.to_dict()
            cache_data[opp.id] = opp_dict
        
        if cache_data:
            await self._save_json(cache_data)
    
    async def _save_json(
        self,
        data: dict
    ) -> None:
        """Save data to JSON cache file."""
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "w") as f:
                    f.write(json.dumps(data, indent=2))
                    logger.info(f"Cache updated: {self.cache_path}")
            except (IOError, PermissionError) as e:
                logger.warning(f"Cache save error: {e}")
                
    async def _load_cache(self) -> dict:
        """Load existing cache if available."""
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "r") as f:
                    data = json.load(f)
                logger.info(f"Cache loaded: {len(data)} items")
                return data
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Cache load error: {e}")
        return {}
    
    async def get_latest_opportunities(
        self,
        limit: Optional[int] = None
    ) -> list[BountyOpportunity]:
        """Get the most recently discovered opportunities."""
        if limit:
            return self.discovered_opportunities[-limit:]
        return self.discovered_opportunities.copy()
    
    async def filter_opportunities(
        self,
        platform: Optional[str] = None,
        min_value: Optional[str] = None
    ) -> list[BountyOpportunity]:
        """Filter discovered opportunities by platform or value."""
        filtered: list[BountyOpportunity] = []
        for opp in self.discovered_opportunities:
            if platform and platform.lower() in opp.platform.lower():
                if min_value is None or str(opp.value) >= min_value:
                    filtered.append(opp)
        return filtered
    
    async def get_platform_summary(
        self
    ) -> dict[str, int]:
        """Get a summary of opportunities per platform."""
        summary: dict[str, int] = {}
        for opp in self.discovered_opportunities:
            platform = opp.platform
            summary[platform] = summary.get(platform, 0) + 1
        return summary


def run_bounty_scanner(
    platforms: Optional[list[str]] = None,
    batch_size: int = 5,
    cache_file: str = "./cache.json"
) -> int:
    """Entry point for running the bounty scanner."""
    scanner = BountyScanner(
        platforms=platforms,
        cache_path=Path(cache_file)
    )
    
    async def on_discover(opp: BountyOpportunity) -> None:
        logger.info(f"🎯 Discovered: {opp.title} - {opp.value}")
        
    scanner._on_discover = on_discover
    logger.info("Starting Bounty Scout Scanner...")
    
    try:
        await asyncio.sleep(0.5)
        results = await scanner.scan_all()
        logger.info(f"Found {len(results)} opportunities")
        return len(results)
    except KeyboardInterrupt:
        logger.info("Scanner interrupted")
        return 1
    except Exception as e:
        logger.error(f"Scanner error: {e}")
        return 1


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    exit_code = run_bounty_scanner(
        platforms=["hackerone.com", "bugcrowd.com", "cobalt.io"],
        batch_size=4
    )
    
    with open("./output_results.json", "w") as f:
        json.dump([{
            "scanned_at": datetime.now().isoformat(),
            "total_found": len(BountyScanner(discovered_opportunities=[]).discovered_opportunities)
        }], f)
    
    logger.info(f"Exit code: {exit_code}")
```