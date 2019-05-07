import os
import xml.etree.ElementTree as et
import pandas as pd
from datetime import datetime


def get_timevsdepth(well):

    report_list = os.listdir('Reports')

    time = []
    md = []
    section = []
    summary = []

    df = pd.DataFrame(
        list(zip(
            time,
            md,
            section,
            summary
        )),
        columns = [
            'Time',
            'MD (m)',
            'Section (in)',
            'Summary'
    ])

    os.chdir('Reports')

    for file in report_list:
        if file[:-15] == well:
            report_tree = et.parse(file)
            report_root = report_tree.getroot()

            time = []
            md = []
            section = []
            summary = []
            time_temp = True
            md_temp = True
            section_temp = True
            summary_temp = True

            for child in report_root:
                for elem in child:
                    if elem.tag == '{http://www.witsml.org/schemas/1series}statusInfo':
                        for subelem in elem:
                            if subelem.tag == '{http://www.witsml.org/schemas/1series}dTim':
                                time.append(datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M'))
                                time_temp = False
                            elif subelem.tag == '{http://www.witsml.org/schemas/1series}md':
                                md.append(float(subelem.text) if float(subelem.text)>0 else 0)
                                md_temp = False
                            elif subelem.tag == '{http://www.witsml.org/schemas/1series}diaHole':
                                section.append(float(subelem.text))
                                section_temp = False
                            elif subelem.tag == '{http://www.witsml.org/schemas/1series}sum24Hr':
                                summary.append(subelem.text)
                                summary_temp = False
                            else:
                                pass

            if time_temp:
                time.append('None')
            if md_temp:
                md.append(0)
            if section_temp:
                section.append('-')
            if summary_temp:
                summary.append('-')

            df = df.append(
                pd.DataFrame(
                    list(zip(
                        time,
                        md,
                        section,
                        summary
                    )),
                    columns = [
                        'Time',
                        'MD (m)',
                        'Section (in)',
                        'Summary'
                    ]),
                ignore_index = True,
                sort = False
            )

    df.sort_values(['Time'], inplace=True)
    os.chdir('../')
    return df


def get_operations(well):

    report_list = os.listdir('Reports')

    start = []
    end = []
    md = []
    operation = []
    comment = []
    duration = []
    state = []

    df = pd.DataFrame(
        list(zip(
            start,
            end,
            md,
            duration,
            operation,
            comment,
            state
        )),
        columns = [
            'Start',
            'End',
            'MD (m)',
            'Duration',
            'Operation',
            'Comment',
            'State'
    ])

    os.chdir('Reports')

    for file in report_list:
        if file[:-15] == well:
            report_tree = et.parse(file)
            report_root = report_tree.getroot()

            start = []
            end = []
            md = []
            operation = []
            comment = []
            duration = []
            state = []

            for child in report_root:
                for elem in child:
                    if elem.tag == '{http://www.witsml.org/schemas/1series}activity':
                        for subelem in elem:
                            if 'dTimStart' in subelem.tag:
                                start.append(datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M'))
                                start_temp = datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M')
                            elif 'dTimEnd' in subelem.tag:
                                end.append(datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M'))
                                end_temp = datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M')
                            elif 'md' in subelem.tag:
                                md.append(subelem.text)
                            elif 'proprietaryCode' in subelem.tag:
                                operation.append(subelem.text)
                            elif 'comments' in subelem.tag:
                                comment.append(subelem.text)
                            elif 'stateDetailActivity' in subelem.tag:
                                state.append(subelem.text)
                            else:
                                pass
                        duration.append((end_temp-start_temp))

            df = df.append(
                pd.DataFrame(
                    list(zip(
                        start,
                        end,
                        md,
                        duration,
                        operation,
                        comment,
                        state
                    )),
                    columns = [
                        'Start',
                        'End',
                        'MD (m)',
                        'Duration',
                        'Operation',
                        'Comment',
                        'State'
                    ]),
                ignore_index = True,
                sort = False
            )

    df.sort_values(['Start'], inplace=True)
    os.chdir('../')
    return df
