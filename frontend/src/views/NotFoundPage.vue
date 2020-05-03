<template>
  <section>
    <h3>Page inconnue :(</h3>
    <br />
    <hr />
    <div class="row actions text-center justify-content-end">
      <div class="col-sm-4">
        <HomeLink />
      </div>
    </div>
  </section>
</template>

<script>
import HomeLink from '../components/HomeLink.vue'

export default {
  name: 'NotFoundPage',
  components: {
    HomeLink,
  }
}
</script>
