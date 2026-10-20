# Persoonlijke Open WebUI + Hermes voor een gedeelde Spark

Route: browser → Open WebUI → Hermes → vLLM op de Spark.

## Starten

1. Pak het pakket uit. Bewaar ook het verborgen bestand `.env`.
2. Vul in `.env` alleen `SPARK_IP` in: het IP-adres van de Spark.
3. Voer in deze map uit: `docker compose up -d`.
4. Open http://localhost:3000 en maak je account aan. Het eerste account wordt beheerder.
5. Selecteer `hermes-agent` als het niet al geselecteerd is.

Docker Engine met Compose v2 of Docker Desktop is nodig. De Spark moet vanaf de Docker-containers bereikbaar zijn op poort 8000, met een OpenAI-compatible vLLM API en werkende tool calling. De Spark-configuratie wordt niet gewijzigd.

Het initialisatiescript vraagt `/v1/models` op en selecteert het enige aangeboden model. Bij meerdere modellen vul je `SPARK_MODEL` in. Bij beveiligde vLLM vul je ook `SPARK_API_KEY` in. Een afwijkende poort stel je in met `SPARK_PORT`.

De contextlimiet wordt uit `max_model_len` overgenomen indien beschikbaar, anders wordt 16384 gebruikt. Als jouw server een andere limiet heeft, vul je `SPARK_CONTEXT` expliciet in. Stel deze nooit hoger in dan de server toestaat.

## Wat vooraf is ingesteld

- Open WebUI maakt uitsluitend verbinding met jouw Hermes-container.
- Hermes gebruikt de Spark als custom modelprovider.
- Een willekeurige interne Hermes API-sleutel wordt automatisch aangemaakt en bewaard.
- Gesprekken, agentgeheugen, skills en werkbestanden blijven bewaard in Docker-volumes.
- Hermes werkt in `/opt/data/workspace`; terminalopdrachten draaien binnen de Hermes-container.
- Geen GPU nodig op de computer waar dit pakket draait.
- Hermes' API wordt niet op een hostpoort gepubliceerd.

Dit is één persoonlijke agentomgeving. Meerdere accounts in deze Open WebUI delen dezelfde Hermes, inclusief geheugen en bestanden. Voor een agent per persoon draait iedereen een eigen kopie van dit pakket, bij voorkeur op de eigen computer. Gebruik bij meerdere kopieën op dezelfde host verschillende Compose-projectnamen (`docker compose -p jeroen up -d`) en verschillende WEBUI_PORT-waarden.

De webinterface is standaard alleen lokaal bereikbaar. Voor gebruik vanaf een andere computer: stel `WEBUI_BIND=0.0.0.0` in en gebruik http://IP-VAN-DEZE-HOST:3000 op het vertrouwde netwerk. Gebruik voor externe toegang een passende HTTPS/reverse-proxy-opzet.

Cloudtools zoals online zoeken of image generation kunnen aanvullende accounts/sleutels vereisen; die zijn niet vooraf ingericht. Er is geen Docker-socket of hostbestandssysteem gekoppeld aan Hermes.

## Beheer

Logs: `docker compose logs -f init hermes open-webui`

Stoppen zonder gegevensverlies: `docker compose down`

Spark-adres/model wijzigen: pas `.env` aan, voer `docker compose down` uit en daarna `docker compose up -d`. De initservice werkt de modelconfiguratie bij en laat overige Hermes-instellingen staan.

Images bijwerken: `docker compose pull`, vervolgens `docker compose down` en `docker compose up -d`. Dit pakket gebruikt bewegende image-tags (Hermes latest / Open WebUI main); leg na een geslaagde proef de image-digests vast voor reproduceerbare uitrol.

## Validatie en grenzen

De YAML en Python zijn statisch gecontroleerd en de initialisatie is getest tegen een gesimuleerde vLLM-modelendpoint. De volledige containers zijn hier niet gestart: Docker en jouw Spark zijn in deze omgeving niet beschikbaar. Controleer op jouw host met `docker compose config` en een eerste chat of de hele keten werkt. Healthchecks bewijzen op zichzelf geen geslaagde modelaanroep.

## Documentatie

- https://hermes-agent.nousresearch.com/docs/user-guide/docker
- https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- https://docs.openwebui.com/reference/env-configuration/
