param(
    [string]$RepoName = "financial-analysis-dashboard",
    [string]$Visibility = "public" # or 'private'
)

# Requires GitHub CLI (gh) installed and authenticated (gh auth login)
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "'gh' CLI not found. Install from https://cli.github.com and run 'gh auth login' before using this script."
    exit 1
}

# Initialize git repo if not already
if (-not (Test-Path .git)) {
    git init
}

# Create remote repo via gh
$exists = gh repo view $RepoName --json name --jq '.name' 2>$null
if ($LASTEXITCODE -ne 0) {
    gh repo create $RepoName --$Visibility --source=. --remote=origin --push
} else {
    Write-Output "Repository $RepoName already exists on your GitHub account. Setting remote and pushing..."
    $remoteUrl = gh repo view $RepoName --json sshUrl --jq '.sshUrl'
    git remote remove origin 2>$null
    git remote add origin $remoteUrl
    git add .
    git commit -m "Initial commit" 2>$null
    git push -u origin main
}

Write-Output "Done. Repository created and code pushed to GitHub."
