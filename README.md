# JC Comparativo

O **JC Comparativo** é um painel de acompanhamento da produção diária. Ele consolida resultados de várias operações e mostra como o desempenho do dia se compara ao último dia útil e a uma referência de produção, como meta ou recorde.

## Demonstração de portfólio

A demonstração usa quatro operações fictícias. O painel mostra a produção por operação e o total consolidado, com diferenças em reais e em percentual. O seletor permite alternar entre meta e recorde.

O calendário de exemplo inclui um feriado na sexta-feira. Ao exibir a produção de segunda-feira, o painel usa a quinta-feira como último dia útil.

## Como executar

Use Python 3.10 ou superior. A demonstração utiliza a biblioteca padrão do Python.

```bash
python jc_comparativo_demo.py
```

Abra [o painel local](http://127.0.0.1:8000) no navegador. Selecione **Meta** ou **Recorde** e clique em **Aplicar**. Para encerrar, pressione **Ctrl+C** no terminal.

## Sobre o projeto original

O aplicativo original utiliza Python, Flask e PostgreSQL para consultar e consolidar a produção. Esta edição gera o painel em Python com dados sintéticos. As consultas, as credenciais e a configuração da operação ficam na versão interna.
