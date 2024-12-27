<template>
  <v-container>
    <v-card>
      <v-card-title>Spectrum Curve</v-card-title>
      <v-card-text>
        <v-row>
          <v-col>
            <v-select
              v-model="selectedDataset"
              :items="datasets"
              label="Select Dataset"
            ></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <canvas id="spectrumChart"></canvas>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="fetchData">Update Chart</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import { Chart } from 'chart.js';
import axios from 'axios';

export default {
  data() {
    return {
      datasets: ["Dataset 1", "Dataset 2"],
      selectedDataset: null,
      chart: null,
    };
  },
  methods: {
    async fetchData() {
      const response = await axios.get("http://127.0.0.1:5000/api/spectrum");
      const data = response.data;
      this.renderChart(data);
    },
    renderChart(data) {
      if (this.chart) this.chart.destroy();
      const ctx = document.getElementById("spectrumChart").getContext("2d");
      this.chart = new Chart(ctx, {
        type: "line",
        data: {
          labels: data.wavelengths,
          datasets: [
            {
              label: "Spectrum Curve",
              data: data.values,
              borderColor: "blue",
            },
          ],
        },
      });
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>