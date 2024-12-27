<template>
  <div>
    <el-select v-model="selectedYears" multiple placeholder="Select years" style="width: 300px;" @change="fetchData">
      <el-option v-for="year in years" :key="year" :label="year" :value="year"></el-option>
    </el-select>
    <el-button type="primary" @click="updateSpeed">Update Speed</el-button>
    <canvas ref="chart" style="width: 100%; max-width: 800px;"></canvas>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import Chart from 'chart.js/auto';

// 创建 Axios 实例并配置拦截器
const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api', // 替换为你的 API 基础 URL
});

// 添加请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 添加响应拦截器
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // 处理 401 错误，例如重定向到登录页面
      console.error('Unauthorized access:', error);
      ElMessage.error('Unauthorized access. Please log in again.');
      // this.$router.push('/login'); // 如果使用 Vue Router
    }
    return Promise.reject(error);
  }
);

export default {
  name: "Spectrum-x",
  data() {
    return {
      years: [],
      selectedYears: [],
      spectrumData: [],
      chart: null,
    };
  },
  async mounted() {


    try {
      const response = await apiClient.get('http://localhost:5000/api/years');
      this.years = response.data;
      console.log('years:', this.years);
    } catch (error) {
      ElMessage.error('Failed to fetch years.');
      console.error('Error details----:', error);
    if (error.response && error.response.status === 422) {
      console.error('Validation errors-----:', error.response.data);
    } else {
      console.error('Error details:', error);
    }
    }
  },
  methods: {
    async fetchData() {
      console.log('Fetching data for years:', this.selectedYears);
      try {
        const response = await apiClient.get('/spectrum', {
          params: { year: this.selectedYears.join(',') },
        });
        this.spectrumData = response.data;
        console.log('Fetched spectrum data:', this.spectrumData); // 打印数据
        this.renderChart();
    } catch (error) {
      ElMessage.error('获取 spectrum data 数据失败.');
      console.error(error);
    }
    },
    renderChart() {
      console.log('Rendering chart with data:', this.spectrumData); // 打印数据
      if (this.chart) this.chart.destroy();

      // 创建一个映射，以便快速查找每个年份的数据
      const yearDataMap = {};
      this.selectedYears.forEach(year => {
        yearDataMap[year] = this.spectrumData.filter(d => d.year === year);
      });

      const ctx = this.$refs.chart.getContext('2d');
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.spectrumData.map(d => d.wavelength).filter((value, index, self) => self.indexOf(value) === index), // 去重波长作为标签
          datasets: this.selectedYears.map(year => ({
            label: `Year ${year}`,
            data: yearDataMap[year].map(d => d.value), // 使用 'value' 字段
            borderColor: `#${Math.floor(Math.random() * 16777215).toString(16)}`, // 随机颜色
            fill: false, // 不填充线条下方区域
          })),
        },
        options: {
          responsive: true,
          scales: {
            x: {
              title: {
                display: true,
                text: 'Wavelength'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Value'
              }
            }
          }
        }
      });
    },
    async updateSpeed() {
      const speedStr = prompt("Enter new speed:");
      const idStr = prompt("Enter data ID to update:");

      if (!speedStr || !idStr) {
        ElMessage.warning('Please enter both speed and data ID.');
        return;
      }

      const speed = parseFloat(speedStr); // 确保 'speed' 是浮点数
      const id = parseInt(idStr, 10); // 确保 'id' 是整数

      if (isNaN(speed) || isNaN(id)) {
        ElMessage.warning('Invalid input. Please enter valid numbers.');
        return;
      }

      try {
        await apiClient.post('/spectrum/speed', { id, speed });
        ElMessage.success('Speed updated!');
      } catch (error) {
        ElMessage.error('Failed to update speed.');
        console.error('Error details:', error.response?.data);
      }
    },
  },
};
</script>

<style scoped>
/* 如果需要自定义样式，可以在这里添加 */
</style>