# AWS_File_Manager

## Descrição

AWS File Manager é uma aplicação web desenvolvida em Python utilizando Streamlit que permite o gerenciamento de arquivos e pastas diretamente no Amazon S3. A aplicação oferece funcionalidades para listar, visualizar, baixar e excluir arquivos, além de gerenciar buckets de forma segura e eficiente.

### File Manager ###  
""" Background """

Há necessidade de disponibilizar uma interface controlada para gestão de arquivos em um bucket S3 que também contém conteúdo sensível não acessível aos usuários operacionais. O sistema deve atuar como uma camada de governança entre os usuários e a AWS, impedindo acesso direto ao console e restringindo qualquer operação apenas aos prefixos pastas.

A solução será uma aplicação web com frontend em React + Tailwind, backend FastAPI, autenticação via AWS Cognito e armazenamento no Amazon S3. O backend operará com uma IAM Role própria e nunca repassará credenciais AWS ao usuário final. O acesso ao bucket será reforçado com políticas explícitas de negação fora dos prefixos autorizados.

O objetivo principal é permitir listagem, criação e deleção de subpastas, upload e remoção de imagens, e trilha de auditoria, mantendo baixa latência, baixo custo operacional e forte isolamento de segurança.

**Requirements**

- Autenticar usuários por login e senha validados em banco de dados próprio.

- Não permitir acesso direto dos usuários ao console da AWS. 
  Login, Logout

- Permitir navegação apenas nos prefixos das pastas selecionadas.

- Listar subpastas e arquivos dentro desses prefixos autorizados.

- Criar subpastas por meio da criação de prefixos no S3.

- Excluir arquivos individualmente.

- Excluir pastas de forma recursiva, removendo todos os objetos sob o prefixo.

- Permitir upload apenas de arquivos .jpg, .jpeg e .tif.

- Impedir, na aplicação e na camada IAM/S3, qualquer acesso fora dos prefixos autorizados.

- Registrar auditoria mínima de login, upload, deleção e criação de pasta.

**Should have**

- Upload direto para o S3 com URL pré-assinada.

- Visualização de miniaturas para imagens.

- Confirmação dupla para exclusão de pasta.

- Versionamento habilitado no bucket para recuperação operacional. """