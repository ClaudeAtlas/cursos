# Cursos de Gobstones

Los seis cursos publicados de Gobstones, **migrados a Gobstones 4** y en un solo lugar.

| Carpeta                  | Curso                                       | De dónde sale                                                                              |
| ------------------------ | ------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `curso-InPr-UNQ`         | Introducción a la programación — UNQ        | [gobstonescursos/curso-InPr-UNQ](https://github.com/gobstonescursos/curso-InPr-UNQ)           |
| `curso-lpysd1`           | La programación y su didáctica 1            | [gobstonescursos/curso-lpysd1](https://github.com/gobstonescursos/curso-lpysd1)               |
| `curso-lpysd2`           | La programación y su didáctica 2            | [gobstonescursos/curso-lpysd2](https://github.com/gobstonescursos/curso-lpysd2)               |
| `curso-lpysd2-virtual`   | La programación y su didáctica 2 — virtual  | [gobstonescursos/curso-lpysd2-virtual](https://github.com/gobstonescursos/curso-lpysd2-virtual) |
| `proyectos-gobstones-jr` | Manual Program.AR                           | [Program-AR/proyectos-gobstones-jr](https://github.com/Program-AR/proyectos-gobstones-jr)     |
| `quell`                  | Quell                                       | [gobstonesgames/quell](https://github.com/gobstonesgames/quell)                               |

`courses.json` es el índice: nombre, carpeta y repositorio de origen de cada uno. Adentro de
cada carpeta está el `guides.json` del curso, con sus guías y sus ejercicios, tal como lo
define el formato del GobstonesWeb.

## Por qué existe

Para que empaquetar un curso en la versión de escritorio no requiera convertir nada al
abrirlo, y para tener el material en un solo lugar en vez de en cinco repositorios de tres
organizaciones distintas.

**Todo está en Gobstones 4.** Se migró con
[`gobstones-migrate`](https://github.com/ClaudeAtlas/Gobstones/tree/main/packages/migrate),
ejercicio por ejercicio, y cada archivo se compiló después de convertirlo. De 304
ejercicios, cuatro no compilan: son plantillas con huecos `...` para que el estudiante
complete, o están en una carpeta llamada `Eliminados`. Tampoco compilaban antes.

## Qué se le sacó

Nada de contenido. Lo que se fue es formato repetido:

| Qué                                                        | Cuánto      |
| ---------------------------------------------------------- | ----------- |
| `.odt`, `.pdf` y `.xcf`: la fuente y la versión imprimible | **82 MB**   |
| Vestimentas copiadas en cada ejercicio del mismo curso     | **51 MB**   |
| Imágenes metidas en base64 adentro del markdown            | **26 MB**   |

- **Los PDF y ODT** son la versión imprimible y la fuente de consignas que ya existen como
  markdown. Las consignas que los enlazan lo hacen **por URL absoluta al repositorio de
  origen**, que sigue publicado, así que sacarlos de acá no rompe ningún enlace.
- **Las vestimentas** se nombran por nombre en el `meta.yml`, no por ruta, y quien las carga
  busca primero la del ejercicio y después la de la raíz del curso. Así que la versión que
  más se repetía se movió a la raíz y se borraron las copias **idénticas**; los 64
  ejercicios que tenían una versión propia se la quedaron.
- **Las imágenes en base64** ya existían como archivo al lado de su consigna en 406 de los
  414 casos: ahora el markdown las referencia en vez de traerlas adentro. Las otras 8 se
  extrajeron.

De 486 MB a 335 MB, y sin tocar una línea de consigna ni una imagen que alguien vea.

## Los originales siguen donde estaban

Este repositorio es **material listo para usar**, no la fuente. Cada curso tiene además su
fork en esta organización, sincronizado con su repositorio de origen: de ahí se traen los
cambios de arriba y se vuelve a armar esto.
