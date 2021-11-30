# Tom Scott Banhammer Generator
> Generates GIFs based on Tom Scott's Banhammer

![Example Banhammer GIF](https://i.imgur.com/l1CdgDm.gif)

## Deploying
GitHub Actions builds Docker images automatically. These can be found in this repo's [Container Registry](https://github.com/nerdcubed/banhammer/pkgs/container/banhammer).

There are additional images for systems that support AVX2 and SSE4 which use an alternative image processing system to speed up generation.

## Usage
Simply send a GET request to `/:text` where `:text` is the text you want displayed in the GIF.
The resulting GIF will be returned and cached for at least 20 minutes.

## Font Licensing
The font file included is a modified version of the Bungee Regular font. The font has been modified to include missing unicode characters and emoji provided by other fonts. The licensing and source information can be found below.

| Font | Designers | Licenses |
| ---- | ---------------- | ------- |
|[Bungee Regular](https://fonts.google.com/specimen/Bungee)|[David Jonathan Ross](http://www.djr.com/)|[SIL Open Font License](assets/Bungee-LICENSE.txt)
|[Twitter Color Emoji SVGinOT Font](https://github.com/twitter/twemoji)|[Brad Erickson](https://keybase.io/bde), [Joe Loughry](https://cnadocs.com/), Terence Eden, [Twitter, Inc](https://about.twitter.com/en_us/company.html) and collaborators|[Massachusetts Institute of Technology License](assets/twitter-color-emoji-LICENSE.txt)<br/>[Creative Commons Attribution 4.0 International](assets/twitter-color-emoji-LICENSE.txt#L24)
|[DejaVu Sans Mono](https://dejavu-fonts.github.io/)|[Štěpán Roh](http://alivebutsleepy.srnet.cz/) and [authors](https://dejavu-fonts.github.io/Authors.html), [Bitstream, Inc](https://www.monotype.com/), [Tavmjung Bah](https://tavmjong.free.fr/)|[Massachusetts Institute of Technology License](assets/Dejau-MIT.txt)
|[Tetsubin Gothic](http://fontna.com/freefont/?p=12)|[フォントな自由](http://fontna.com/)|[Apache License 2.0](assets/Tetsubin-LICENSE.txt)
