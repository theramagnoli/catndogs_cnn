<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

const file = ref<File | null>(null);
const prediction = ref<string | null>(null);
const error = ref<string | null>(null);

async function imageToBase64(file: File) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
}

async function setFile(event: Event) {
  const target = event.target as HTMLInputElement;
  const files = target.files as FileList;
  file.value = files[0];

  const base64_image = await imageToBase64(file.value);
  const uploaded_imageElement = document.getElementById(
    "uploaded_image",
  ) as HTMLImageElement;

  uploaded_imageElement.src = base64_image as string;
}

async function sendImageToApi() {
  if (file.value === null) return;
  try {
    const formData = new FormData();
    formData.append("image", file.value);

    const response = await axios.post(
      "http://localhost:5000/api/predict",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "*",
          "Access-Control-Allow-Headers": "*",
        },
      },
    );

    const data = response.data;
    prediction.value = data.prediction;
  } catch (err) {
    error.value = err.message ?? "Error desconocido";
  }
}

function clear() {
  file.value = null;
  prediction.value = null;
  error.value = null;
}
</script>

<template>
  <div class="max-w-3xl mx-auto my-16">
    <h1 class="text-7xl font-black text-indigo-500">¿Perro o gato?</h1>
    <p class="text-2xl text-gray-400 mt-6">
      Sube una imagen y descubre si es un perro o un gato
    </p>
    <input
      v-if="prediction === null && file === null"
      type="file"
      accept=".jpg, .jpeg, .png"
      class="mt-6 block w-full text-transparent text-[0px] file:mr-4 file:py-4 file:px-8 file:rounded-full file:border-0 file:font-semibold file:bg-indigo-50 file:text-indigo-500 hover:file:bg-indigo-100 file:font-sans file:cursor-pointer file:text-2xl file:tracking-wider hover:file:tracking-widest file:transition-all file:lowercase active:file:scale-90"
      @change="setFile"
    />
    <button
      v-else-if="prediction === null"
      class="mt-6 rounded-full py-4 px-8 bg-indigo-500 text-white font-semibold text-2xl hover:bg-indigo-600 transition-all tracking-wider hover:tracking-widest lowercase active:scale-90 disabled:opacity-50 disabled:cursor-not-allowed"
      @click="sendImageToApi"
    >
      descubrir
    </button>
    <button
      v-else
      class="mt-6 rounded-full py-4 px-8 bg-indigo-500 text-white font-semibold text-2xl hover:bg-indigo-600 transition-all tracking-wider hover:tracking-widest lowercase active:scale-90 disabled:opacity-50 disabled:cursor-not-allowed"
      @click="clear"
    >
      limpiar
    </button>

    <div class="relative">
      <img
        src=""
        alt="Imagen subida"
        v-show="file !== null"
        id="uploaded_image"
        class="mt-6 rounded-3xl border-8 border-indigo-50 max-w-[400px] max-h-[400px] min-w-[400px] min-h-[400px] object-contain bg-indigo-50"
      />
      <p
        class="mt-6 text-2xl absolute bottom-0 left-0 w-[400px] py-8 px-8 bg-green-500 rounded-b-2xl font-semibold text-white"
        v-if="prediction !== null && error === null"
      >
        Es un {{ prediction === "dog" ? "perro" : "gato" }}
      </p>
      <p
        class="mt-6 text-2xl absolute bottom-0 left-0 w-[400px] py-8 px-8 bg-red-500 rounded-b-2xl font-semibold text-white overflow-hidden"
        v-if="error !== null"
      >
        Ocurrió un error: {{ error }}
      </p>
    </div>
  </div>
</template>

<style></style>
