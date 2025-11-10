# PowerShell script to update the news section of the dashboard with more recent articles
# This script will fetch recent energy news and update the dashboard HTML

# Function to fetch recent news from RSS feeds
function Get-RecentEnergyNews {
    param(
        [int]$MaxItems = 10
    )
    
    # RSS feeds for energy news
    $rssFeeds = @(
        "https://news.google.com/rss/search?q=oil+gas+LNG+energy+prices&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=energy+commodities&hl=en-US&gl=US&ceid=US:en"
    )
    
    $allNews = @()
    
    foreach ($feedUrl in $rssFeeds) {
        try {
            $feedContent = Invoke-WebRequest -Uri $feedUrl -UseBasicParsing -TimeoutSec 10
            $xml = [xml]$feedContent.Content
            
            foreach ($item in $xml.rss.channel.item | Select-Object -First 10) {
                $newsItem = [PSCustomObject]@{
                    Title = $item.title
                    Link = $item.link
                    Published = $item.pubDate
                    Source = $xml.rss.channel.title
                }
                $allNews += $newsItem
            }
        }
        catch {
            Write-Warning "Failed to fetch news from $feedUrl"
        }
    }
    
    # Sort by published date and return top items
    return $allNews | Sort-Object {[DateTime]$_.Published} -Descending | Select-Object -First $MaxItems
}

# Function to update the news section in the dashboard HTML
function Update-DashboardNewsSection {
    param(
        [string]$DashboardPath = "dashboard.html",
        [array]$NewsItems
    )
    
    # Read the dashboard HTML
    $dashboardContent = Get-Content $DashboardPath -Raw
    
    # Find the news section
    $newsSectionPattern = '(?s)(<div class="news-section">.*?<div class="card-title">Market News</div>).*?(</div>\s*</div>\s*</div>)'
    
    if ($dashboardContent -match $newsSectionPattern) {
        $beforeNews = $dashboardContent.Substring(0, $dashboardContent.IndexOf($matches[1]))
        $afterNews = $dashboardContent.Substring($dashboardContent.IndexOf($matches[2]) + $matches[2].Length)
        
        # Generate new news items HTML
        $newsItemsHtml = ""
        foreach ($item in $NewsItems) {
            $newsItemsHtml += @"
                <div class="news-item">
                    <a href="$($item.Link)" target="_blank" class="news-title">$($item.Title)</a>
                    <div class="news-meta">
                        <span class="news-source">$($item.Source)</span>
                        <span class="news-date">$($item.Published)</span>
                    </div>
                </div>
                
"@
        }
        
        # Create the new news section
        $newNewsSection = @"
<div class="news-section">
            <div class="card-title">Market News</div>
            $newsItemsHtml
        </div>
"@
        
        # Combine everything
        $newDashboardContent = $beforeNews + $newNewsSection + $afterNews
        
        # Write back to file
        $newDashboardContent | Out-File -FilePath $DashboardPath -Encoding UTF8
        Write-Host "News section updated successfully!" -ForegroundColor Green
    }
    else {
        Write-Warning "Could not find news section in dashboard HTML"
    }
}

# Main execution
Write-Host "Fetching recent energy news..." -ForegroundColor Yellow
$recentNews = Get-RecentEnergyNews -MaxItems 10

if ($recentNews.Count -gt 0) {
    Write-Host "Found $($recentNews.Count) recent news items" -ForegroundColor Green
    Write-Host "Updating dashboard news section..." -ForegroundColor Yellow
    Update-DashboardNewsSection -NewsItems $recentNews
    Write-Host "Dashboard updated successfully!" -ForegroundColor Green
}
else {
    Write-Warning "No recent news found"
}