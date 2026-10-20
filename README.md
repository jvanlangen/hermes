# Persoonlijke Open WebUI + Hermes voor een gedeelde Spark
## Verbinding

```mermaid
flowchart LR
  subgraph computer[Computer van de gebruiker]
    browser[Browser<br/>localhost:3000]
    subgraph docker[Docker-containers]
      webui[Open WebUI]
      hermes[Hermes]
    end
    workspace[workspace-map<br/>inhoud genegeerd door Git]
    browser --> webui
    webui -->|HTTP API| hermes
    workspace -. volume mount .-> hermes
  end
  subgraph pwr[PWR-netwerk]
    spark[DGX Spark<br/>vLLM :8000]
  end
  hermes -->|HTTP API| spark
  webui -->|Direct OpenAI API| spark
```

## Starten

1. Installeer Docker Desktop en clone deze repo.
2. Open PowerShell in de projectmap en start de containers:

   ```powershell
   docker compose up -d
   ```

3. Open http://localhost:3000, maak een account aan en kies `hermes-agent` of `gpt-oss-120b`.

Compose maakt `workspace/` aan als die ontbreekt en koppelt de map aan Hermes. Git negeert alle inhoud van deze map. Alleen deze map is toegankelijk voor Hermes, zodat Hermes geïsoleerd draait.
