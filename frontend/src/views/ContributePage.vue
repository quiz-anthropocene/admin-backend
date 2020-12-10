<template>
  <section class="text-align-left">
    <h2>Contribuer !</h2>

    <p>
      Vous souhaitez rajouter une question ? Ou faire un commentaire sur le contenu existant ?<br />
      Envoyez-nous ça en remplissant le petit formulaire ci-dessous 👇
    </p>

    <br />

    <form @submit.prevent="submitContribution" v-if="!contributionSubmitted">
      <div class="form-group">
        <h3 class="margin-bottom-0">
          <label for="contribution_type">Ma contribution est ...</label>
        </h3>
        <div class="custom-control custom-radio custom-control-inline">
          <input type="radio" id="customRadioInline1" name="customRadioInline1" class="custom-control-input" value="nouvelle question" v-model="contribution.type">
          <label class="custom-control-label" for="customRadioInline1">Une nouvelle question</label>
        </div>
        <div class="custom-control custom-radio custom-control-inline">
          <input type="radio" id="customRadioInline2" name="customRadioInline2" class="custom-control-input" value="nouveau quiz" v-model="contribution.type">
          <label class="custom-control-label" for="customRadioInline2">Une idée de quiz</label>
        </div>
        <div class="custom-control custom-radio custom-control-inline">
          <input type="radio" id="customRadioInline3" name="customRadioInline3" class="custom-control-input" value="commentaire application" v-model="contribution.type">
          <label class="custom-control-label" for="customRadioInline3">Un commentaire sur l'application</label>
        </div>
        <!-- <div class="custom-control custom-radio custom-control-inline">
          <input type="radio" id="customRadioInline3" name="customRadioInline3" class="custom-control-input" value="nom application" v-model="contribution.type">
          <label class="custom-control-label" for="customRadioInline3">Un nom d'application alternatif</label>
        </div> -->
      </div>

      <div class="form-group" v-if="contribution.type === 'nouvelle question'">
        <h3 class="margin-bottom-0">
          <label for="contribution_text">Votre question <span class="color-red">*</span></label>
        </h3>
        <div class="help-text">En 1 ou 2 phrases au maximum</div>
        <input type="text" id="contribution_text" class="form-control" v-model="contribution.text" required />
      </div>
      <div class="form-group" v-if="contribution.type === 'nouvelle question'">
        <h3 class="margin-bottom-0">
          <label for="text">Informations supplémentaires</label>
        </h3>
        <div class="help-text">La réponse et un peu d'explication, un lien pour aller plus loin, ...</div>
        <textarea id="description" class="form-control" rows="5" v-model="contribution.description"></textarea>
      </div>

      <div class="form-group" v-if="contribution.type === 'nouveau quiz'">
        <h3 class="margin-bottom-0">
          <label for="contribution_text">Votre idée de quiz <span class="color-red">*</span></label>
        </h3>
        <div class="help-text">En 1 ou 2 phrases au maximum</div>
        <input type="text" id="contribution_text" class="form-control" v-model="contribution.text" required />
      </div>
      <div class="form-group" v-if="contribution.type === 'nouveau quiz'">
        <h3 class="margin-bottom-0">
          <label for="text">Informations supplémentaires</label>
        </h3>
        <div class="help-text">Des idées de questions, des liens pour creuser le sujet, ...</div>
        <textarea id="description" class="form-control" rows="5" v-model="contribution.description"></textarea>
      </div>

      <div class="form-group" v-if="contribution.type === 'commentaire application'">
        <h3 class="margin-bottom-0">
          <label for="contribution_text">Votre commentaire <span class="color-red">*</span></label>
        </h3>
        <div class="help-text">bug, amélioration, ... Lâchez-vous :)</div>
        <textarea id="contribution_text" class="form-control" rows="5" v-model="contribution.text" required></textarea>
      </div>

      <div class="form-group" v-if="contribution.type === 'nom application'">
        <h3 class="margin-bottom-0">
          <label for="contribution_text">Votre idée <span class="color-red">*</span></label>
        </h3>
        <textarea id="contribution_text" class="form-control" rows="2" v-model="contribution.text" required></textarea>
      </div>

      <br />

      <p>
        🙋&nbsp;Veuillez indiquer votre <strong>email</strong> si voulez être tenu au courant de votre contribution !<br />
      </p>
      <p class="help-text">
        En soumettant ce formulaire, vous autorisez que les informations saisies soient traitées afin d'améliorer notre application, et vous recontacter si besoin.
      </p>

      <div class="form-group">
        <p>
          <button type="submit" class="btn" :class="contribution.text ? 'btn-primary' : 'btn-outline-primary'" :disabled="!contribution.text">📩&nbsp;Envoyer !</button>
        </p>
      </div>
    </form>

    <div v-if="contributionSubmitted && loading" class="loading">
      Envoi de votre contribution...
    </div>

    <div v-if="contributionSubmitted && error" class="error">
      <h3>Il y a eu une erreur 😢</h3>
      {{ error }}
    </div>

    <div v-if="contributionSubmitted && contributionResponse">
      <h3>Merci beaucoup 💯</h3>
      <p>On fera de notre mieux pour prendre en compte votre contribution.</p>
      <div v-if="contributionSubmitted" @click="init()">
        <a href="#">✍️&nbsp;Nouvelle contribution</a>
      </div>
    </div>
  </section>
</template>

<script>
import { metaTagsGenerator } from '../utils';

export default {
  name: 'Contribute',
  metaInfo() {
    const title = 'Contribuer';
    const description = 'Contribuer à l\'application pour la faire grandir !';
    return {
      title,
      meta: metaTagsGenerator(title, description),
    };
  },
  components: {
  },

  data() {
    return {
      contribution: {
        text: '',
        description: '',
        type: 'nouvelle question',
      },
      contributionSubmitted: false,
      contributionResponse: null,
      loading: false,
      error: null,
    };
  },

  mounted() {
    if (this.$route.query.type) {
      this.init(this.$route.query.type);
    } else {
      this.init();
    }
  },

  methods: {
    init(typeFromQuery) {
      this.contribution = {
        text: '',
        description: '',
        type: typeFromQuery || 'nouvelle question',
      };
      this.contributionSubmitted = false;
      this.contributionResponse = null;
      this.loading = false;
      this.error = null;
    },
    submitContribution() {
      this.contributionSubmitted = true;
      this.error = this.contributionResponse = null;
      this.loading = true;
      fetch(`${process.env.VUE_APP_API_ENDPOINT}/contribute`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.contribution),
      })
        .then((response) => {
          this.loading = false;
          return response.json();
        })
        .then((data) => {
          this.contributionResponse = data;
        })
        .catch((error) => {
          console.log(error);
          this.error = error;
        });
    },
  },
};
</script>
