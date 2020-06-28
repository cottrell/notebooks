<template>
  <div class="main">
    <h1>Main</h1>
    Something here.
    <MainComponent msg="Main here" />
  </div>
</template>

<script>
// @ is an alias to /src
import MainComponent from "@/components/Main.vue";

export default {
  name: "Main",
  components: {
    MainComponent,
  }
};
</script>
