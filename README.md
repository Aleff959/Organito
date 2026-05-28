# 📁 Organito

> Sua pasta de Downloads não deveria parecer um depósito. Arquivos têm tipos, tipos têm lugar. Sem configuração complexa, sem nuvem, sem rastreamento — apenas organização local, rápida e reversível.

---

**Organito** é um aplicativo de desktop moderno desenvolvido em **Python 3**, utilizando a interface gráfica **GTK4** e a biblioteca **libadwaita** (seguindo as diretrizes do Material Design 3 / GNOME). Ele foi criado para trazer ordem ao caos dos seus diretórios locais, agrupando seus arquivos baixados em pastas organizadas por categorias inteligentes de forma rápida e segura.

## ✨ Funcionalidades

* **Organização Inteligente por Categorias:** Reconhece e separa automaticamente centenas de extensões de arquivos divididas em 13 categorias:
  * 🖼️ **Imagens** (incluindo formatos RAW como `.cr2`, `.nef`, `.arw`)
  * 📄 **Documentos** (`.pdf`, `.docx`, `.md`, etc.)
  * 📊 **Planilhas** (`.xlsx`, `.csv`, `.ods`, etc.)
  * 📉 **Apresentações** (`.pptx`, `.key`, etc.)[cite: 1]
  * 🎬 **Vídeos** (`.mp4`, `.mkv`, `.mov`, etc.)[cite: 1]
  * 🎵 **Áudio** (incluindo áudio profissional e lossless como `.wav`, `.flac`, `.opus`)[cite: 1]
  * 📦 **Compactados** (`.zip`, `.rar`, `.7z`, `.tar.gz`, etc.)[cite: 1]
  * 🚀 **Instaladores** (`.deb`, `.rpm`, `.exe`, `.msi`, `.appimage`, etc.)[cite: 1]
  * 💻 **Código** (suporta dezenas de linguagens: `.py`, `.js`, `.kt`, `.rs`, `.json`, `.yaml`, etc.)[cite: 1]
  * 🔤 **Fontes** (`.ttf`, `.otf`, `.woff2`)[cite: 1]
  * 🗄️ **Banco de Dados** (`.sqlite`, `.db`, `.sql`, etc.)[cite: 1]
  * 📐 **3D e CAD** (`.stl`, `.obj`, `.blend`, `.dwg`, etc.)[cite: 1]
  * 🧲 **Torrents e P2P** (`.torrent`)[cite: 1]
* **Interface Moderna e Fluida:** Menu hambúrguer nativo com navegação simplificada entre as abas Início, Configurações, Sistema, Ajuda e Sobre[cite: 1].
* **Gerenciamento de Temas:** Suporte total a tema Claro, Escuro ou Automático (seguindo a preferência do sistema operacional)[cite: 1].
* **Configurações Avançadas e Persistentes:** Salva suas preferências automaticamente em `~/.config/organito/settings.json` (no Linux) ou no `APPDATA` (no Windows)[cite: 1].
* **Abas de Controle Técnico:**
  * **Aba Sistema:** Exibe informações detalhadas de hardware e do sistema operacional em tempo real (OS, Kernel, CPU, RAM, Uso de Disco, e versões do Runtime GTK/libadwaita)[cite: 1].
  * **Modo Dry Run:** Permite simular a organização completa para ver os logs do que seria feito sem mover de fato nenhum arquivo[cite: 1].
  * **Processamento Recursivo:** Opção para organizar arquivos dentro de subpastas com limite customizável de profundidade[cite: 1].
  * **Filtros de Tamanho:** Filtra arquivos por tamanho mínimo ou máximo (em KB)[cite: 1].
  * **Controle de Desempenho:** Permite limitar a quantidade máxima de arquivos processados por vez e adicionar pausas em milissegundos entre as movimentações (ideal para poupar escritas intensas em SSDs)[cite: 1].
  * **Logs Completos:** Opção para salvar relatórios detalhado com data e hora de cada operação realizada[cite: 1].
* **Segurança e Proteção de Dados:**
  * Tratamento inteligente e automático para conflitos de nomes (Renomear adicionando sufixo numérico, Pular ou Substituir)[cite: 1].
  * Suporte para mover os arquivos para a Lixeira do sistema em vez de mover diretamente, tornando o processo 100% reversível (requer `send2trash`)[cite: 1].
  * Tratamento automático de arquivos ocultos (`.`), arquivos temporários (`.tmp`, `.crdownload`, `.part`) e arquivos de sistema (`thumbs.db`, `.DS_Store`, `desktop.ini`)[cite: 1].
  * Detecção de plataforma com tratamento específico para o Windows (ex: bloqueio de nomes reservados como `CON`, `PRN`, `NUL` e suporte a caminhos longos)[cite: 1].

## 🗂️ Estrutura do Projeto

```text
organito/
├── organito_1.0_all.deb               # Pacote de instalação Debian/Ubuntu
├── README.md                          # Documentação do projeto
├── src/                               # Código-fonte principal
│   ├── main.py                        # Entrypoint do aplicativo
│   ├── core.py                        # Lógica interna e mapeamento de categorias
│   ├── ui.py                          # Interface gráfica em GTK4/libadwaita e CSS
│   ├── settings.py                    # Gerenciamento e persistência de configurações JSON
│   └── sysinfo.py                     # Coleta multiplataforma de métricas de sistema
├── data/                              # Recursos e metadados
│   ├── io.github.aleff959.Organito.desktop     # Arquivo Desktop do Linux
│   ├── io.github.aleff959.Organito.metainfo.xml # Metainfo AppStream
│   └── icons/                                   # Ícones da aplicação em múltiplos tamanhos
└── tests/                             # Suíte de testes automatizados
    └── test_core.py                   # Testes unitários da lógica de organização
