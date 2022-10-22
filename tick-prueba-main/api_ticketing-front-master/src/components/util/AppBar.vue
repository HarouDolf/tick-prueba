<template>
<v-app-bar color="" app>
	<v-div class="text-center">
	</v-div>
	<template >
			<v-div >
			<v-avatar :size=35>
				<img  src="@/assets/global.png"/>
			</v-avatar>
			<select
			class="mx-2"
			v-model="$i18n.locale"
			@change="updateLanguage($event.target.value)"
			variant="info">mdi-chevron-down
			<option
			hide-details
			v-for="(o, i) in locales_array"
			:key="i"
			:value="o.value"
			:selected="o.value === locale_default"
			> {{ o.caption }}
			</option>
			</select>
			</v-div>
		</template>
</v-app-bar>
</template>
<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import { LOCALES, Locales } from "@/locales/i18n";
	import defaultLocale from "@/i18n";
	@Component({
		name: 'AppBar',
	})
	
	export default class AppBar extends Vue {
		public locales_array = LOCALES;
		public locale_default = defaultLocale;
		public updateLanguage(lang: Locales) {
			console.log("cambiando idioma a ", lang);
			this.$emit('changeEvent', lang);
		}

	}
</script>
