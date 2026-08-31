# PRD: .NET 5 → .NET 8 Cloud-Native Migration

> **Workshop Use:** Practice exercise for [Module 2 — Legacy Codebase Modernization](../legacy-modernization.md). Demonstrates agy strict mode, agent self-onboarding with AGENTS.md, subagent planning, and `ctrl+g` plan editing. The target repository includes a reference `modernization-prompt.md` authored by GCP Cloud Solutions Architects — a gold-standard example of prompt engineering for migration tasks.

!!! example "Video Walkthrough: Ex08 Dotnet Modernization"
    <video controls width="100%" poster="../assets/videos/ex08_poster.png">
      <source src="../assets/videos/ex08_dotnet_modernization.mp4" type="video/mp4">
      Download video: [ex08_dotnet_modernization.mp4](../assets/videos/ex08_dotnet_modernization.mp4)
    </video>

---

## Problem

A partially-upgraded ASP.NET application (ContosoUniversity) runs on .NET 5 with Entity Framework 6 and the legacy Generic Host pattern (`Startup.cs` + `Program.cs`). .NET 5 reached end of support in May 2022. The app uses SQL Server-flavored EF6 but needs to target Cloud Run with PostgreSQL. It lacks containerization, structured logging, and graceful shutdown handling.

## Business Drivers

| Driver | Impact |
| :-- | :-- |
| **Security compliance** | .NET 5 is EOL — no security patches. Blocks compliance certification. |
| **Deployment speed** | From manual VM deployment to 3-minute container push on Cloud Run |
| **Scalability** | Cloud Run auto-scales from 0 to N instances based on traffic |
| **Cost** | Eliminate Windows Server licensing — Linux containers on Cloud Run cost ~70% less |
| **Data layer** | Migrate from EF6/SQL Server to EF Core 8/PostgreSQL for managed Cloud SQL |

## Target Repository

[ContosoUniversity — Google Cloud .NET Modernization Demo](https://github.com/GoogleCloudPlatform/cloud-solutions/tree/main/projects/dotnet-modernization-demo)

The repo provides both the legacy app (`dotnet-migration-sample/`) and the completed target state (`dotnet-migration-sample-modernized/`) for self-verification. Students work exclusively in the `dotnet-migration-sample/` directory.

```bash
git clone --depth 1 https://github.com/GoogleCloudPlatform/cloud-solutions.git
cd cloud-solutions/projects/dotnet-modernization-demo/dotnet-migration-sample
```

> **Bonus resource:** The repo includes [`modernization-prompt.md`](https://github.com/GoogleCloudPlatform/cloud-solutions/blob/main/projects/dotnet-modernization-demo/modernization-prompt.md) — a 225-line production-grade migration prompt from the GCP team. Compare your agent's approach with this reference to study prompt engineering for migration tasks.

## Scope

### In Scope

- Upgrade target framework from .NET 5 to .NET 8
- Replace Generic Host pattern (`Startup.cs`) with minimal hosting API (`WebApplication.CreateBuilder()`)
- Migrate Entity Framework 6 to Entity Framework Core 8
- Switch database provider from SQL Server to PostgreSQL (Npgsql)
- Create a Cloud Run-compliant Dockerfile and Docker Compose configuration
- Implement structured logging, PORT binding, and SIGTERM graceful shutdown

### Out of Scope

- Business logic changes (faithful 1:1 feature replication)
- Frontend redesign (Razor views stay as-is, just ensure they compile)
- Database schema changes (EF Core should map to equivalent schema)

## Migration Checklist

### Phase 0: Context Engineering — Agent Self-Onboarding

Before writing migration code, the agent should build its own understanding of the codebase.

- [ ] **Set strict mode** — prevent accidental file writes during investigation:

  ```text
  /permissions strict
  ```

- [ ] **Investigate the codebase:**

  ```text
  Analyze the ContosoUniversity application. Map:
  1. Current framework version and all NuGet dependencies
  2. The Startup.cs/Program.cs hosting pattern
  3. All System.Data.Entity (EF6) usage across DAL, controllers, and migrations
  4. Configuration sources (appsettings.json, web.config remnants)
  5. Google Cloud integrations (Diagnostics, logging)
  ```

- [ ] **Generate a migration-aware AGENTS.md** based on the analysis
- [ ] **Review and approve** the generated AGENTS.md before proceeding
- [ ] **Switch to request-review mode** before Phase 1:

  ```text
  /permissions request-review
  ```

### Phase 1: TFM and Package Upgrade

- [ ] Update `ContosoUniversity.csproj`: change `<TargetFramework>net5.0</TargetFramework>` → `net8.0`
- [ ] Update all NuGet packages to .NET 8-compatible versions:
  - `Microsoft.AspNetCore.Mvc.NewtonsoftJson` → 8.0.x
  - `System.ComponentModel.Annotations` → 8.0.x
  - `System.Configuration.ConfigurationManager` → 8.0.x
  - `Google.Cloud.Diagnostics.AspNetCore` → latest 8.0-compatible
- [ ] Remove the `Microsoft.DotNet.UpgradeAssistant.Extensions.Default.Analyzers` package (no longer needed)
- [ ] Remove `<GenerateAssemblyInfo>false</GenerateAssemblyInfo>` and delete `Properties/AssemblyInfo.cs`
- [ ] Run `dotnet restore` — resolve any package conflicts

### Phase 2: Hosting Modernization

- [ ] Replace `Startup.cs` + `Program.cs` (Generic Host pattern) with minimal hosting API:

  ```csharp
  var builder = WebApplication.CreateBuilder(args);
  builder.Services.AddControllersWithViews();
  // ... service registration
  var app = builder.Build();
  // ... middleware pipeline
  app.Run();
  ```

- [ ] Move `ConfigureServices()` body into the top-level `builder.Services` block
- [ ] Move `Configure()` body into the top-level `app.Use*()` pipeline
- [ ] Migrate `CreateHostBuilder` secret config loading to the new pattern
- [ ] Configure PORT binding for Cloud Run: `app.Run("http://0.0.0.0:" + port)`
- [ ] Add SIGTERM graceful shutdown handler
- [ ] Delete `Startup.cs` after migration is complete

### Phase 3: Entity Framework 6 → EF Core 8

- [ ] Remove `EntityFramework` 6.4.4 package
- [ ] Add `Microsoft.EntityFrameworkCore` and `Npgsql.EntityFrameworkCore.PostgreSQL` 8.0.x
- [ ] Refactor `SchoolContext`:
  - Replace `System.Data.Entity` imports → `Microsoft.EntityFrameworkCore`
  - Replace `DbModelBuilder` → `ModelBuilder` in `OnModelCreating`
  - Remove `PluralizingTableNameConvention` → add explicit `.ToTable()` calls
  - Remove `MapToStoredProcedures()` (not supported in EF Core)
  - Replace constructor `SchoolContext(string connectString) : base(connectString)` → `SchoolContext(DbContextOptions<SchoolContext> options) : base(options)`
- [ ] Register DbContext in DI: `builder.Services.AddDbContext<SchoolContext>(options => options.UseNpgsql(...))`
- [ ] Refactor `SchoolInitializer.cs` → `DbInitializer.cs` using `context.Database.EnsureCreated()`
- [ ] Remove `SchoolConfiguration.cs` (`Database.SetInitializer<T>()` is EF6-only)
- [ ] Remove `SchoolInterceptorLogging.cs` and `SchoolInterceptorTransientErrors.cs` (EF6 interceptors) → replace with EF Core logging via `ILoggerFactory`
- [ ] Delete all EF6 migration files (`Migrations/2014*.cs`, `Migrations/Configuration.cs`)
- [ ] Update all controllers to remove `System.Data.Entity` imports and fix `RetryLimitExceededException` (EF6) → EF Core equivalent
- [ ] Run `dotnet build` — fix all compilation errors

### Phase 4: Containerization & Cloud Run

- [ ] Create multi-stage `Dockerfile`:

  ```dockerfile
  FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
  WORKDIR /src
  COPY . .
  RUN dotnet publish -c Release -o /app

  FROM mcr.microsoft.com/dotnet/aspnet:8.0
  WORKDIR /app
  COPY --from=build /app .
  USER 1000
  EXPOSE 8080
  ENTRYPOINT ["dotnet", "ContosoUniversity.dll"]
  ```

- [ ] Add `.dockerignore` (exclude `bin/`, `obj/`, `.git/`)
- [ ] Create `compose.yaml` with PostgreSQL + app services:
  - PostgreSQL container with `pg_isready` healthcheck
  - App container with connection string via environment variable
  - No `version` attribute (deprecated in Compose Spec)
- [ ] Configure structured JSON logging for Cloud Logging: `builder.Logging.AddJsonConsole()`
- [ ] Run `docker build --check .` — pass all Docker build checks
- [ ] Run `docker compose up --build --detach` — verify the app starts and database initializes

### Phase 5: Validation & Testing

- [ ] `dotnet build` compiles without errors or warnings
- [ ] Docker image builds and runs on Linux (not Windows containers)
- [ ] Container runs as non-root user (UID 1000)
- [ ] All HTTP endpoints respond correctly (GET, POST for CRUD operations)
- [ ] Database is initialized with seed data on first run
- [ ] Application handles anti-forgery tokens correctly for POST/DELETE operations
- [ ] Structured JSON logs appear in `docker compose logs`
- [ ] No connection strings or credentials in source code

## What the Agent Should Do

This PRD is designed to test the agent's ability to:

1. **Bootstrap its own context** — use strict mode + codebase investigation to write an AGENTS.md before starting (Phase 0)
2. **Understand legacy patterns** — recognize EF6 idioms (`DbModelBuilder`, interceptors, `Database.SetInitializer`) and map them to EF Core equivalents
3. **Follow a phased plan** — use `ctrl+g` to edit and approve the plan before executing
4. **Perform mechanical refactoring** — the EF6 → EF Core migration touches every controller and model file
5. **Verify its own work** — run `dotnet build` and `docker compose up` after each phase
6. **Use `/rewind`** if a phase goes wrong — this is your checkpoint, not a failure

## Acceptance Criteria

- [ ] An `AGENTS.md` exists in the project root encoding the migration context
- [ ] `dotnet build` compiles without errors on .NET 8
- [ ] No `System.Data.Entity` imports remain anywhere in the codebase
- [ ] No `Startup.cs` — app uses minimal hosting API in `Program.cs`
- [ ] `EntityFramework` 6.x package fully replaced by `Microsoft.EntityFrameworkCore` 8.x
- [ ] Docker image builds and runs on Linux with non-root user
- [ ] `docker compose up` successfully starts app + PostgreSQL and seeds the database
- [ ] No connection strings or credentials in source code
- [ ] Application responds to health check within 2 seconds of cold start
