# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json

from django import forms

from haystack.query import SearchQuerySet


class BaseBulkAddFormSet(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        if 'parties' in kwargs:
            self.parties = kwargs['parties']
            del kwargs['parties']
        if 'source' in kwargs:
            self.source = kwargs['source']
            del kwargs['source']
        super(BaseBulkAddFormSet, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        super(BaseBulkAddFormSet, self).add_fields(form, index)
        form.fields["party"] = forms.ChoiceField(
            choices=self.parties,
            widget=forms.Select(attrs={
                'class': 'party-select',
            }),
        )

        if 'party' in getattr(form, '_hide', []):
            form.fields["party"].widget = forms.HiddenInput()

        if hasattr(self, 'source'):
            form.fields["source"].initial = self.source
            form.fields["source"].widget = forms.HiddenInput()


class BaseBulkAddReviewFormSet(BaseBulkAddFormSet):
    def suggested_people(self, person_name):
        return SearchQuerySet().filter(content=person_name)[:5]

    def format_value(self, suggestion):
        """
        Turn the whole form in to a value string
        """
        return [suggestion.pk, suggestion.name]

    def add_fields(self, form, index):
        super(BaseBulkAddReviewFormSet, self).add_fields(form, index)
        suggestions = self.suggested_people(form['name'].value())

        CHOICES = [('_new', 'Add new person')]
        if suggestions:
            CHOICES += [self.format_value(suggestion)
                for suggestion in suggestions]
        form.fields['select_person'] = forms.ChoiceField(
            choices=CHOICES, widget=forms.RadioSelect())

        form.fields["party"] = forms.ChoiceField(
            choices=self.parties,
            widget=forms.HiddenInput(attrs={
                'readonly':'readonly',
                'class': 'party-select',
            }),
            required=False
        )


class QuickAddSinglePersonForm(forms.Form):
    name = forms.CharField(required=True)
    source = forms.CharField(required=True)


class ReviewSinglePersonForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'readonly':'readonly'}))
    source = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'readonly':'readonly'}))


BulkAddFormSet = forms.formset_factory(
    QuickAddSinglePersonForm,
    extra=15,
    formset=BaseBulkAddFormSet)


BulkAddReviewFormSet = forms.formset_factory(
    ReviewSinglePersonForm,
    extra=0,
    formset=BaseBulkAddReviewFormSet)


