from django.shortcuts import render
from django.views.generic import TemplateView

import csv


class InflationView(TemplateView):
    template_name = 'inflation.html'

    def get(self, request, *args, **kwargs):
        with open('inflation_russia.csv', encoding='utf-8') as file_contents:
            contents = csv.reader(file_contents, delimiter=';')
            rows_list = list()
            for row in contents:
                row_list = list()
                for item in row:
                    if item:
                        row_list.append(item)
                    else:
                        row_list.append('-')
                rows_list.append(row_list)
            context = {
                'header': rows_list[0],
                'data': rows_list[1:]
                       }
            return render(request, self.template_name, context)