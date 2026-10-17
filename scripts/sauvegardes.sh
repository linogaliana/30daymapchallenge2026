#!/usr/bin/env bash
# Copie sur le S3 du SSP Cloud les fichiers sources listés dans jours/_liens/sauvegardes.yml.
#
# Pour chaque entrée, télécharge la source (curl) et l'écrit à l'adresse de substitution, où
# https://minio.lab.sspcloud.fr/ devient s3:// (aws s3 cp). Un fichier déjà présent sur le S3
# n'est pas réécrit, sauf avec --force true.
#
#     bash scripts/sauvegardes.sh               # ne copie que les fichiers absents
#     bash scripts/sauvegardes.sh --force true  # recopie tout
#
# Le YAML est écrit par scripts/sauvegardes.py. Identifiants et point d'accès S3 : variables
# AWS_* du SSP Cloud (AWS_ENDPOINT_URL, ou à défaut AWS_S3_ENDPOINT).

set -euo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
YAML="$RACINE/jours/_liens/sauvegardes.yml"
PREFIXE_HTTPS="https://minio.lab.sspcloud.fr/"

forcer=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      if [[ "${2:-}" == "true" || "${2:-}" == "false" ]]; then
        forcer="$2"; shift 2
      else
        forcer=true; shift
      fi
      ;;
    --force=true|--force=false) forcer="${1#--force=}"; shift ;;
    -h|--help) sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Argument inconnu : $1 (attendu : --force true|false)" >&2; exit 2 ;;
  esac
done

# Point d'accès S3 : aws le lit dans AWS_ENDPOINT_URL ; sinon on le construit depuis AWS_S3_ENDPOINT.
aws_s3=(aws)
if [[ -z "${AWS_ENDPOINT_URL:-}" && -n "${AWS_S3_ENDPOINT:-}" ]]; then
  aws_s3+=(--endpoint-url "https://$AWS_S3_ENDPOINT")
fi

temporaire="$(mktemp -d)"
trap 'rm -rf "$temporaire"' EXIT

# Paires source / substitution, une par ligne, séparées par une tabulation.
paires() {
  sed -nE \
    -e "s/^- source: *['\"]?([^'\"]*)['\"]? *$/\1/p" \
    -e "s/^  substitution: *['\"]?([^'\"]*)['\"]? *$/\1/p" \
    "$YAML" | paste - -
}

copies=0; presents=0; echecs=()
while IFS=$'\t' read -r source substitution; do
  if [[ "$substitution" != "$PREFIXE_HTTPS"* ]]; then
    echo "✗ substitution hors du S3 du SSP Cloud : $substitution" >&2
    echecs+=("$substitution"); continue
  fi
  chemin="${substitution#"$PREFIXE_HTTPS"}"      # lgaliana/30daymapchallenge2026/fichier.csv
  cible="s3://$chemin"
  seau="${chemin%%/*}"
  cle="${chemin#*/}"

  if [[ "$forcer" != true ]] && "${aws_s3[@]}" s3api head-object --bucket "$seau" --key "$cle" >/dev/null 2>&1; then
    echo "· déjà présent : $cible"
    presents=$((presents + 1)); continue
  fi

  # Le fichier temporaire garde le nom de la cible : aws en déduit le Content-Type.
  local_="$temporaire/$(basename "$cle")"
  echo "↓ $source"
  if ! curl --fail --location --silent --show-error --retry 3 --output "$local_" "$source"; then
    echo "✗ échec du téléchargement : $source" >&2
    echecs+=("$source"); continue
  fi
  if ! "${aws_s3[@]}" s3 cp --no-progress "$local_" "$cible"; then
    echo "✗ échec de l'écriture : $cible" >&2
    echecs+=("$cible")
  else
    copies=$((copies + 1))
  fi
  rm -f "$local_"
done < <(paires)

echo
echo "$copies copiés, $presents déjà présents, ${#echecs[@]} échecs."
if [[ ${#echecs[@]} -gt 0 ]]; then
  printf '  %s\n' "${echecs[@]}" >&2
  exit 1
fi
