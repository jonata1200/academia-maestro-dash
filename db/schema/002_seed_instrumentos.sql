-- Inserir Instrumentos
INSERT OR IGNORE INTO instrumentos (id, nome_instrumento) VALUES (1, 'Violão');
INSERT OR IGNORE INTO instrumentos (id, nome_instrumento) VALUES (2, 'Teclado');
INSERT OR IGNORE INTO instrumentos (id, nome_instrumento) VALUES (3, 'Guitarra');
INSERT OR IGNORE INTO instrumentos (id, nome_instrumento) VALUES (4, 'Bateria');
INSERT OR IGNORE INTO instrumentos (id, nome_instrumento) VALUES (5, 'Violino');

-- Inserir Aulas Ofertadas
-- Associando cada aula ao seu instrumento correspondente
INSERT OR IGNORE INTO aulas_ofertadas (id, nome_aula, instrumento_id) VALUES (1, 'Aula de Violão', 1);
INSERT OR IGNORE INTO aulas_ofertadas (id, nome_aula, instrumento_id) VALUES (2, 'Aula de Teclado', 2);
INSERT OR IGNORE INTO aulas_ofertadas (id, nome_aula, instrumento_id) VALUES (3, 'Aula de Guitarra', 3);
INSERT OR IGNORE INTO aulas_ofertadas (id, nome_aula, instrumento_id) VALUES (4, 'Aula de Bateria', 4);
INSERT OR IGNORE INTO aulas_ofertadas (id, nome_aula, instrumento_id) VALUES (5, 'Aula de Violino', 5);

-- Inserir Professores de Exemplo
INSERT OR IGNORE INTO professores (id, nome, email, telefone, especializacao) VALUES (1, 'Ana Silva', 'ana.silva@maestro.com', '11987654321', 'Violão Clássico');
INSERT OR IGNORE INTO professores (id, nome, email, telefone, especializacao) VALUES (2, 'Bruno Mendes', 'bruno.mendes@maestro.com', '11998765432', 'Teclado Pop/Jazz');
INSERT OR IGNORE INTO professores (id, nome, email, telefone, especializacao) VALUES (3, 'Carlos Souza', 'carlos.souza@maestro.com', '11976543210', 'Guitarra Rock/Blues');
INSERT OR IGNORE INTO professores (id, nome, email, telefone, especializacao) VALUES (4, 'Diana Costa', 'diana.costa@maestro.com', '11965432109', 'Bateria Rítmica');
INSERT OR IGNORE INTO professores (id, nome, email, telefone, especializacao) VALUES (5, 'Eduardo Lima', 'eduardo.lima@maestro.com', '11954321098', 'Violino Erudito');

-- Mapear Professores para Instrumentos que Lecionam
-- Ana Silva leciona Violão
INSERT OR IGNORE INTO professores_instrumentos (professor_id, instrumento_id) VALUES (1, 1);
-- Bruno Mendes leciona Teclado
INSERT OR IGNORE INTO professores_instrumentos (professor_id, instrumento_id) VALUES (2, 2);
-- Carlos Souza leciona Guitarra
INSERT OR IGNORE INTO professores_instrumentos (professor_id, instrumento_id) VALUES (3, 3);
-- Diana Costa leciona Bateria
INSERT OR IGNORE INTO professores_instrumentos (professor_id, instrumento_id) VALUES (4, 4);
-- Eduardo Lima leciona Violino
INSERT OR IGNORE INTO professores_instrumentos (professor_id, instrumento_id) VALUES (5, 5);
-- Exemplo: Um professor pode lecionar múltiplos instrumentos
INSERT OR IGNORE INTO professores_instrumentos (professor_id, instrumento_id) VALUES (1, 3); -- Ana também leciona Guitarra