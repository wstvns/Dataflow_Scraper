<template>
  <div class="container">
    <h1>Buscar Operadora</h1>
    <input v-model="termo" @input="buscarOperadora" placeholder="Digite o nome da operadora..." />
    <ul>
      <li v-for="operadora in operadoras" :key="operadora.registro_ans">
        {{ operadora.razao_social }} ({{ operadora.cnpj }})
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      termo: '',
      operadoras: []
    };
  },
  methods: {
    async buscarOperadora() {
      if (this.termo.length > 2) {
        const response = await axios.get(`http://127.0.0.1:5000/buscar_operadora?termo=${this.termo}`);
        this.operadoras = response.data;
      } else {
        this.operadoras = [];
      }
    }
  }
};
</script>

<style>
.container {
  max-width: 600px;
  margin: 20px auto;
  text-align: center;
}
input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  padding: 5px;
  border-bottom: 1px solid #ccc;
}
</style>
