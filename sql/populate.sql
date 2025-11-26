INSERT INTO cliente (nome, cpf, telefone, email, data_nascimento, observacoes) VALUES
('João Silva Santos', '12345678901', '47999887766', 'joao.silva@email.com', '1985-03-15', 'Alérgico a produtos com mentol'),
('Pedro Oliveira Costa', '23456789012', '47988776655', 'pedro.oliveira@email.com', '1990-07-22', NULL),
('Carlos Eduardo Souza', '34567890123', '47977665544', 'carlos.souza@email.com', '1988-11-30', 'Prefere cortes degradê'),
('Lucas Ferreira Lima', '45678901234', '47966554433', 'lucas.lima@email.com', '1995-05-18', NULL),
('Rafael Mendes Alves', '56789012345', '47955443322', 'rafael.alves@email.com', '1992-09-25', 'Cliente VIP'),
('Marcos Paulo Santos', '67890123456', '47944332211', 'marcos.santos@email.com', '1987-01-10', NULL),
('Fernando Costa Silva', '78901234567', '47933221100', 'fernando.silva@email.com', '1993-06-08', 'Gosta de conversar durante o corte'),
('André Luiz Pereira', '89012345678', '47922110099', 'andre.pereira@email.com', '1991-12-14', NULL),
('Bruno Henrique Rocha', '90123456789', '47911009988', 'bruno.rocha@email.com', '1989-04-20', 'Pele sensível'),
('Rodrigo Martins Dias', '01234567890', '47900998877', 'rodrigo.dias@email.com', '1994-08-03', NULL);

INSERT INTO barbeiro (nome, cpf, telefone, email, data_contratacao, especialidade, comissao_percentual) VALUES
('Roberto "Tesoura de Ouro" Silva', '11122233344', '47988887777', 'roberto.silva@barbearia.com', '2020-01-15', 'corte', 35.00),
('Anderson "Barba Perfeita" Costa', '22233344455', '47977776666', 'anderson.costa@barbearia.com', '2020-06-20', 'barba', 30.00),
('Felipe "Designer" Santos', '33344455566', '47966665555', 'felipe.santos@barbearia.com', '2021-03-10', 'designer', 32.00),
('Marcelo "Estilista" Oliveira', '44455566677', '47955554444', 'marcelo.oliveira@barbearia.com', '2021-09-01', 'coloração', 35.00),
('Thiago "Clássico" Pereira', '55566677788', '47944443333', 'thiago.pereira@barbearia.com', '2022-02-14', 'corte', 30.00);

INSERT INTO servico (nome, descricao, preco, duracao_estimada) VALUES
('Corte Simples', 'Corte de cabelo tradicional', 40.00, 30),
('Corte + Barba', 'Corte de cabelo + barba completa', 70.00, 50),
('Barba Completa', 'Aparar, desenhar e finalizar barba', 35.00, 25),
('Designer de Barba', 'Designer e acabamento especial de barba', 45.00, 35),
('Corte Degradê', 'Corte degradê moderno', 50.00, 40),
('Corte + Barba + Sobrancelha', 'Combo completo', 85.00, 60),
('Sobrancelha', 'Designer de sobrancelha masculina', 20.00, 15),
('Platinado/Coloração', 'Coloração ou descoloração capilar', 120.00, 90),
('Luzes/Reflexos', 'Aplicação de luzes ou reflexos', 150.00, 120),
('Tratamento Capilar', 'Hidratação e tratamento', 80.00, 45);

INSERT INTO produto (nome, descricao, preco_venda, estoque_atual, estoque_minimo) VALUES
('Pomada Modeladora', 'Pomada para modelar cabelo - fixação forte', 35.00, 25, 5),
('Cera Modeladora', 'Cera para finalização - fixação média', 32.00, 30, 5),
('Óleo para Barba', 'Óleo hidratante para barba', 45.00, 15, 3),
('Shampoo Anticaspa', 'Shampoo especial anticaspa', 28.00, 40, 8),
('Gel Fixador', 'Gel para cabelo - fixação extra forte', 25.00, 20, 5),
('Balm para Barba', 'Balm hidratante e modelador', 40.00, 18, 3),
('Condicionador', 'Condicionador profissional', 30.00, 35, 8),
('Spray Finalizador', 'Spray para finalização de corte', 38.00, 22, 5),
('Máscara Capilar', 'Máscara de tratamento intensivo', 55.00, 12, 3),
('Talco para Barba', 'Talco pós-barba', 22.00, 28, 5);

INSERT INTO horario_trabalho (id_barbeiro, dia_semana, horario_inicio, horario_fim) VALUES
-- Roberto: Segunda a Sexta (8h às 18h)
(1, 1, '08:00', '18:00'),
(1, 2, '08:00', '18:00'),
(1, 3, '08:00', '18:00'),
(1, 4, '08:00', '18:00'),
(1, 5, '08:00', '18:00'),
-- Anderson: Segunda a Sábado (9h às 19h)
(2, 1, '09:00', '19:00'),
(2, 2, '09:00', '19:00'),
(2, 3, '09:00', '19:00'),
(2, 4, '09:00', '19:00'),
(2, 5, '09:00', '19:00'),
(2, 6, '09:00', '17:00'),
-- Felipe: Terça a Sábado (10h às 20h)
(3, 2, '10:00', '20:00'),
(3, 3, '10:00', '20:00'),
(3, 4, '10:00', '20:00'),
(3, 5, '10:00', '20:00'),
(3, 6, '10:00', '18:00'),
-- Marcelo: Segunda a Sexta (9h às 18h)
(4, 1, '09:00', '18:00'),
(4, 2, '09:00', '18:00'),
(4, 3, '09:00', '18:00'),
(4, 4, '09:00', '18:00'),
(4, 5, '09:00', '18:00'),
-- Thiago: Quarta a Domingo (10h às 20h)
(5, 3, '10:00', '20:00'),
(5, 4, '10:00', '20:00'),
(5, 5, '10:00', '20:00'),
(5, 6, '10:00', '18:00'),
(5, 0, '10:00', '16:00');

INSERT INTO atendimento (id_cliente, id_barbeiro, tipo, data_agendada, horario_agendado, status, data_atendimento) VALUES
(1, 1, 'agendado', CURRENT_DATE + INTERVAL '1 day', '09:00', 'agendado', NULL),
(2, 2, 'agendado', CURRENT_DATE + INTERVAL '1 day', '10:00', 'agendado', NULL),
(3, 3, 'agendado', CURRENT_DATE + INTERVAL '2 days', '14:00', 'agendado', NULL),
(4, 1, 'agendado', CURRENT_DATE + INTERVAL '2 days', '11:00', 'agendado', NULL),
(5, 4, 'agendado', CURRENT_DATE + INTERVAL '3 days', '15:00', 'agendado', NULL);

INSERT INTO atendimento (id_cliente, id_barbeiro, tipo, data_atendimento, horario_inicio, horario_fim, valor_total, forma_pagamento, status, observacoes) VALUES
(1, 1, 'walkin', CURRENT_DATE - INTERVAL '5 days', '09:00', '09:30', 40.00, 'pix', 'finalizado', 'Cliente satisfeito'),
(3, 3, 'walkin', CURRENT_DATE - INTERVAL '3 days', '14:00', '14:40', 50.00, 'dinheiro', 'finalizado', NULL),
(5, 2, 'walkin', CURRENT_DATE - INTERVAL '1 day', '15:00', '15:25', 35.00, 'cartao_credito', 'finalizado', NULL);

INSERT INTO atendimento (id_cliente, id_barbeiro, tipo, data_agendada, horario_agendado, data_atendimento, horario_inicio, horario_fim, valor_total, forma_pagamento, status, observacoes) VALUES
(2, 2, 'agendado', CURRENT_DATE - INTERVAL '4 days', '10:00', CURRENT_DATE - INTERVAL '4 days', '10:05', '10:50', 70.00, 'cartao_debito', 'finalizado', 'Cliente chegou no horário'),
(4, 1, 'agendado', CURRENT_DATE - INTERVAL '2 days', '11:00', CURRENT_DATE - INTERVAL '2 days', '11:00', '11:50', 70.00, 'pix', 'finalizado', NULL);

INSERT INTO atendimento_servico (id_atendimento, id_servico, preco_cobrado) VALUES
(6, 1, 40.00),   -- atendimento 6: walk-in
(7, 2, 70.00),   -- atendimento 7: agendado realizado
(8, 5, 50.00),   -- atendimento 8: walk-in
(9, 2, 70.00),   -- atendimento 9: agendado realizado
(10, 3, 35.00);  -- atendimento 10: walk-in

INSERT INTO venda_produto (id_atendimento, id_produto, quantidade, preco_unitario, subtotal) VALUES
(6, 1, 1, 35.00, 35.00),  
(7, 3, 1, 45.00, 45.00),  
(9, 1, 1, 35.00, 35.00), 
(9, 6, 1, 40.00, 40.00),  
(10, 10, 1, 22.00, 22.00); 