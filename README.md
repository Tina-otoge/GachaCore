# GachaCore

Backend API that aggregate collectibles from many different sources to allow for running virtual gacha on them.

## Currently supported sources

- Azur Lane

  Website: https://azurlane.yo-star.com/

  Resources used:
  - Azur Lane Wiki: https://azurlane.koumakan.jp/wiki/Azur_Lane_Wiki
  - AzurAPI: https://azurapi.github.io/

## Notes

- Running on Termux fails while installing pydantic-core, probably has to do
  with building Rust from source. Use `pip install --only-binary pydantic-core
  -r requirements.txt` to fix.

## TODO

- [ ] Generic abstraction for any source
- [ ] Gacha support
- [ ] Web UI
- [ ] Inventory support
