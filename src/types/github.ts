// Arquivo de tipos existente, apenas garantindo que não há mudanças necessárias aqui
// Mas incluído para completude se a estrutura exigir
export interface Issue {
  number: number;
  title: string;
  body: string;
  labels: string[];
  state: 'open' | 'closed';
}
