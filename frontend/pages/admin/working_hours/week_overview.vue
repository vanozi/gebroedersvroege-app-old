<template>
  <v-container>
        <ConfirmDlg ref="confirm" />
    <v-container>
      <v-row>
        <v-col cols="4" class="justify-left">
          <v-dialog
            ref="dialog"
            v-model="modal"
            :return-value.sync="date"
            persistent
            width="290px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                label="Selecteer data"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
                v-model="dateRangeText"
              ></v-text-field>
            </template>
            <v-date-picker locale="nl-nl" v-model="dates" range>
              <v-spacer></v-spacer>
              <v-btn text color="primary" @click="modal = false">
                Annuleer
              </v-btn>
              <v-btn
                text
                color="primary"
                @click="
                  modal = false;
                  notSubmittedWeeks();
                "
              >
                OK
              </v-btn>
            </v-date-picker>
          </v-dialog>
        </v-col>
      </v-row>

      <v-expansion-panels focusable>
        <v-expansion-panel
          @click.native="setWeekDates(item)"
          v-for="(item, i) in weeks_not_submitted"
          :key="i"
        >
          <v-expansion-panel-header class="subtitle-1"
            >Week {{ item.week }}:&nbsp;<span
              class="subtitle-2 font-weight-light font-italic"
            >
              ({{ item.week_start }} - {{ item.week_end }})</span
            ></v-expansion-panel-header
          >
          <v-expansion-panel-content>
            <v-data-table
              :headers="headers"
              :items="item.employee_info"
              :items-per-page="10"
              class="elevation-1"
            >
              <template #item.submitted="{ item }"
                ><v-icon color="green" v-if="item.submitted">
                  mdi-hand-okay</v-icon
                >
                <v-icon color="red" v-else>
                  mdi-close-octagon-outline</v-icon
                ></template
              >
              <template v-slot:item.acties="{ item }">
                <v-btn
                  small
                  flat
                  color="primary"
                  outlined
                  v-if="item.submitted == true"
                  @click="unlockWeek(item)"
                  >Geef vrij</v-btn
                >
              </template>
            </v-data-table>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-container>
  </v-container>
</template>

<script>
import ConfirmDlg from "~/components/ConfirmDlg.vue";
import { mapGetters, mapActions } from "vuex";
import moment from "moment";
export default {
  data: () => ({
    modal: false,
    weekStart: null,
    weekEnd: null,
    dateformat: "YYYY-MM-DD",
    today: moment().format("YYYY-MM-DD"),
    from_date: moment().subtract(4, "weeks").format("YYYY-MM-DD"),
    to_date: moment().subtract().format("YYYY-MM-DD"),
    dates: [
      moment().subtract(4, "weeks").format("YYYY-MM-DD"),
      moment().subtract().format("YYYY-MM-DD"),
    ],
    weeks_not_submitted: null,
    headers: [
      {
        text: "Naam",
        value: "name",
        sortable: true,
      },
      {
        text: "Tot. uren",
        value: "sum_hours",
        sortable: false,
      },
      {
        text: "Ingediend?",
        value: "submitted",
        sortable: false,
      },
      {
        text: "Acties",
        value: "acties",
        sortable: false,
      },
    ],
  }),
  methods: {
    ...mapActions({
      getAllUsers: "users/getUsers",
      addWorkingHoursToAllUsersState:
        "working_hours/addWorkingHoursToAllUsersState",
      resetAll: "working_hours/resetStateAllUsersAllWorkingHours",
    }),
    setWeekDates(item) {
      this.weekStart = item.week_start;
      this.weekEnd = item.week_end;
      console.log(item);
    },
    async unlockWeek(item) {
            if (
        await this.$refs.confirm.open(
          "Bevestig",
          "Weet je zeker dat je de uren voor deze week wilt vrijgeven?"
        )
      )
      // Login API call
      try {
        let response = await this.$axios.get(
          "/working_hours/admin/unlock_week",
          {
            params: {
              from_date: this.weekStart,
              to_date: this.weekEnd,
              user_id: item.user_id,
            },
          }
        );
        this.notSubmittedWeeks();
      } catch (err) {
        if (err.response) {
          this.$notifier.showMessage({
            content: err.response.data.detail,
            color: "error",
          });
        }
      }
    },

    async notSubmittedWeeks() {
      // Login API call
      try {
        let response = await this.$axios.get(
          "/working_hours/admin/week_overview",
          { params: { from_date: this.dates[0], to_date: this.dates[1] } }
        );
        this.weeks_not_submitted = response.data.reverse();
      } catch (err) {
        if (err.response) {
          this.$notifier.showMessage({
            content: err.response.data.detail,
            color: "error",
          });
        }
      }
    },
  },
  computed: {
    dateRangeText() {
      const sortedDates = this.dates.sort((a, b) => moment(a).diff(b));
      console.log(sortedDates);
      return sortedDates.join(" ~ ");
    },
    workingHoursPerWeekInSelectedYear() {
      var usersNotSubmittedForWeeksInYear = [];
      var date = moment(String(this.computedSelectedYear)).startOf("year");
      if (this.computedSelectedYear == moment().year()) {
        var endDate = moment().endOf("isoweek");
      } else {
        var endDate = moment(String(this.computedSelectedYear)).endOf("year");
      }

      while (date <= endDate) {
        var beginningOfWeek = moment(date)
          .startOf("isoweek")
          .format(this.dateformat);
        var endOfWeek = moment(date).endOf("isoweek").format(this.dateformat);
        var weekNumber = moment(date).isoWeek();

        var users_not_submitted = [];

        for (const user of this.get_all_working_hours_all_users) {
          var working_hours = user.working_hours;
          var hoursWeek = working_hours.filter(
            (item) =>
              moment(item.date) >= moment(beginningOfWeek) &&
              moment(item.date) <= moment(endOfWeek)
          );
          if (hoursWeek.length === 0) {
            var weekIsSubmitted = false;
            users_not_submitted.push(
              user.user.first_name + " " + user.user.last_name
            );
          } else {
            var weekIsSubmitted = hoursWeek.every(function (e) {
              console.log(e.submitted);
              return e.submitted === true;
            });
          }
        }
        usersNotSubmittedForWeeksInYear.push({
          week_number: weekNumber,
          start_of_week: beginningOfWeek,
          end_of_week: endOfWeek,
          not_submitted: users_not_submitted,
        });
        date = date.add(7, "days");
      }
      return usersNotSubmittedForWeeksInYear.reverse();
    },
    // Getters from the store
    // mix the getters into computed with object spread operator
    ...mapGetters({
      users: "users/Users",
      // users met rol werknemer
      werknemers: "users/Werknemers",
      working_hours: "working_hours/get_all_working_hours",
      get_all_working_hours_all_users:
        "working_hours/get_all_working_hours_all_users",
    }),
    computedSelectedYear() {
      return this.today ? moment(this.today).isoWeekYear() : "";
    },
  },
  created() {
    this.notSubmittedWeeks();
  },
};
</script>

<style>
</style>