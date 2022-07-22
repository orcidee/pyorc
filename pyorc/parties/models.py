import re
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS_PENDING = 0
STATUS_VALIDATED = 1
STATUS_REFUSED = 2
STATUS_CANCELLED = 3

STATUS = (
    (STATUS_PENDING, _("en attente de validation")),
    (STATUS_VALIDATED, _("validée")),
    (STATUS_REFUSED, _("refusée")),
    (STATUS_CANCELLED, _("annulée")),
)


def current_year():
    return datetime.today().year


class PartyType(models.Model):
    name = models.CharField(_("Nom affiché"), max_length=200)
    codename = models.CharField(_("Nom unique"), max_length=100)
    is_table_number_required = models.BooleanField(_("Requiert un numéro de table"))
    is_availability_required = models.BooleanField(
        _("Requiert une vérification de disponibilité")
    )
    order = models.SmallIntegerField(_("Ordre d'affichage"), default=0)

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return self.name


class Party(models.Model):
    # Autoincrement number with a year prefix
    id = models.PositiveBigIntegerField(_("ID"), primary_key=True, blank=True)

    # Hidden technical useful field
    created_at = models.DateTimeField(_("Date de création"), default=datetime.now)

    # Displayed fields
    party_type = models.ForeignKey(
        PartyType, on_delete=models.PROTECT, verbose_name=_("Type de partie")
    )
    name = models.CharField(_("Nom de la partie"), max_length=200)
    scenario_name = models.CharField(_("Nom du scénario"), max_length=200, blank=True)
    is_desk_registration = models.BooleanField(_("Inscription au stand"), default=False)
    desk_name = models.CharField(_("Nom du stand"), max_length=200, blank=True)

    # FIXME Should be displayed as required if is_desk_registration is False
    min_players = models.PositiveIntegerField(
        _("Nombre minimum de participant·exs"),
        validators=[MinValueValidator(1), MaxValueValidator(300)],
        blank=True,
        null=True,
    )
    max_players = models.PositiveIntegerField(
        _("Nombre maximum de participant·exs"),
        validators=[MinValueValidator(1), MaxValueValidator(300)],
        blank=True,
        null=True,
    )

    # FIXME: Should be displayed only when party_type is JDR, JDP ou Figurines
    table_amount = models.PositiveIntegerField(
        _("Nombre de table(s) requise(s)"), default=1
    )

    # FIXME: Use a RTF widget (b, i, u, link, ul, ol, align, preview)
    description = models.TextField(_("Description"), max_length=3000)

    note_to_organizers = models.TextField(_("Note aux organisateur·icexs"), blank=True)
    year = models.PositiveIntegerField(
        _("Année de la convention"), default=current_year
    )

    start = models.DateTimeField(_("Date et heure de début"))
    duration = models.PositiveIntegerField(_("Durée en minutes"))

    status = models.SmallIntegerField(_("Status actuel"), choices=STATUS)

    # TODO
    # Tags (multiselect) => CF. Autre ticket
    # Tableau des dispos \* => CF. Autre ticket

    class Meta:
        ordering = ["-year", "-start", "-created_at"]
        verbose_name_plural = "parties"

    def __str__(self):
        return f"{self.name} ({self.id})"

    def clean(self):
        if self.is_desk_registration:
            if not self.desk_name:
                raise ValidationError(
                    {
                        "desk_name": _(
                            "Le nom du stand est requis si l'inscription est au stand"
                        )
                    }
                )
        else:
            if not self.min_players:
                raise ValidationError(
                    {"min_players": _("Nombre minimum de participant·exs est requis.")}
                )
            if not self.max_players:
                raise ValidationError(
                    {"max_players": _("Nombre maximum de participant·exs est requis.")}
                )

        if self.duration % 30 != 0:
            raise ValidationError(
                {"duration": _("La durée en minutes doit être un multiple de 30.")}
            )

        if self.id and not str(self.id).startswith(str(self.year)):
            raise ValidationError(
                {"year": _("L'année ne peut être modifiée une fois la partie crée.")}
            )

    def save(self, *args, **kwargs):
        # Set the ID, by year with an auto increment
        if self.id is None:
            year = current_year()
            this_year_max = (
                self.__class__.objects.filter(id__startswith=year)
                .order_by("-id")
                .first()
            )
            if this_year_max:
                new_id = int(
                    "{}{}".format(
                        year,
                        int(
                            re.match(
                                "{}{}".format(year, r"(\d*)"), str(this_year_max.id)
                            ).group(1)
                        )
                        + 1,
                    )
                )
            else:
                new_id = int(f"{year}1")
            self.id = new_id

        super().save(*args, **kwargs)
