import iomb.refmap as ref


def append_data_quality(process: dict, sector: ref.Sector):
    process['dqSystem'] = {
        '@type': 'DQSystem',
        '@id': '812283e0-e5a0-48af-8835-1abc34f236f0'}
    process['exchangeDqSystem'] = {
        '@type': 'DQSystem',
        '@id': 'd9dd0e5e-2b67-45b3-acbb-2e632550dd46'}
    if sector.data_quality_entry is not None:
        process['dqEntry'] = sector.data_quality_entry


def dq_exchanges_system() -> dict:
    s = {
        '@context': 'http://greendelta.github.io/olca-schema/context.jsonld',
        '@type': 'DQSystem',
        '@id': 'd9dd0e5e-2b67-45b3-acbb-2e632550dd46',
        'name': 'USEEIO - Data Quality - Flows',
        'hasUncertainties': False, 'summable': True,
        'indicators': [
            {
                'name': 'Reliability', 'position': 1,
                'scores': [
                    {
                        'position': 1, 'label': '1',
                        'description': 'Verified data based on measurements'
                    },
                    {
                        'position': 2, 'label': '2',
                        'description': 'Verified data partly based on '
                                       'assumptions or non-verified data '
                                       'based on measurements'
                    },
                    {
                        'position': 3, 'label': '3',
                        'description': 'Non-verified data partly based on '
                                       'qualified estimates'
                    },
                    {
                        'position': 4, 'label': '4',
                        'description': 'Qualified estimate (e.g. by industrial '
                                       'expert)'
                    },
                    {
                        'position': 5, 'label': '5',
                        'description': 'Non-qualified estimates'
                    }
                ]
            },
            {
                'name': 'Temporal correlation', 'position': 2,
                'scores': [
                    {
                        'position': 1, 'label': '1',
                        'description': 'Less than 3 years of difference to the '
                                       'time period of the data set'
                    },
                    {
                        'position': 2, 'label': '2',
                        'description': 'Less than 6 years of difference to the '
                                       'time period of the data set'
                    },
                    {
                        'position': 3, 'label': '3',
                        'description': 'Less than 10 years of difference to '
                                       'the time period of the data set'
                    },
                    {
                        'position': 4, 'label': '4',
                        'description': 'Less than 15 years of difference to '
                                       'the time period of the data set'
                    },
                    {
                        'position': 5, 'label': '5',
                        'description': 'Age of data unknown or more than 15 '
                                       'years of difference to the time period '
                                       'of the data set'
                    }
                ]
            },
            {
                'name': 'Geographical correlation', 'position': 3,
                'scores': [
                    {
                        'position': 1, 'label': '1',
                        'description': 'Data from area under study'
                    },
                    {
                        'position': 2, 'label': '2',
                        'description': 'Average data from larger area in which '
                                       'the area under study is included'
                    },
                    {
                        'position': 3, 'label': '3',
                        'description': 'Data from area with similar production '
                                       'conditions'
                    },
                    {
                        'position': 4, 'label': '4',
                        'description': 'Data from area with slightly similar '
                                       'production conditions'
                    },
                    {
                        'position': 5, 'label': '5',
                        'description': 'Data from unknown or distinctly '
                                       'different area (North America instead '
                                       'of Middle East, OECD-Europe instead '
                                       'of Russia)'
                    }
                ]
            },
            {
                'name': 'Technological correlation', 'position': 4,
                'scores': [
                    {
                        'position': 1, 'label': '1',
                        'description': 'Data from enterprises, processes and '
                                       'materials under study'
                    },
                    {
                        'position': 2, 'label': '2',
                        'description': 'Data from processes and materials '
                                       'under study (i.e. identical '
                                       'technology)  but from different '
                                       'enterprises'
                    },
                    {
                        'position': 3, 'label': '3',
                        'description': 'Data from processes and materials '
                                       'under study but from different '
                                       'technology'
                    },
                    {
                        'position': 4, 'label': '4',
                        'description': 'Data on related processes or materials'
                    },
                    {
                        'position': 5, 'label': '5',
                        'description': 'Data on related processes on '
                                       'laboratory scale or from different '
                                       'technology'
                    }
                ]},
            {
                'name': 'Data collection', 'position': 5,
                'scores': [
                    {
                        'position': 1, 'label': '1',
                        'description': 'Representative data from all sites '
                                       'relevant for the market considered, '
                                       'over and adequate period to even out '
                                       'normal fluctuations',
                    },
                    {
                        'position': 2, 'label': '2',
                        'description': 'Representative data from \u003e 50% of '
                                       'the sites relevant for the market '
                                       'considered, over an adequate period '
                                       'to even out normal fluctuations',
                    },
                    {
                        'position': 3, 'label': '3',
                        'description': 'Representative data from only some '
                                       'sites (\u003c\u003c 50%) relevant for '
                                       'the market considered or \u003e 50% of '
                                       'sites but from shorter periods',
                    },
                    {
                        'position': 4, 'label': '4',
                        'description': 'Representative data from only one site '
                                       'relevant for the market considered or '
                                       'some sites but from shorter periods',
                    },
                    {
                        'position': 5, 'label': '5',
                        'description': 'Representativeness unknown or data '
                                       'from a small number of sites and from '
                                       'shorter periods',
                    }
                ]
            }
        ]
    }
    return s


def dq_process_system() -> dict:
    s = {
        '@context': 'http://greendelta.github.io/olca-schema/context.jsonld',
        '@type': 'DQSystem',
        '@id': '812283e0-e5a0-48af-8835-1abc34f236f0',
        'name': 'USEEIO - Data Quality - Processes',
        'hasUncertainties': False, 'summable': True,
        'indicators': [
            {
                'name': 'Review', 'position': 1,
                'scores': [
                    {
                        'position': 1, 'label': '1',
                        'description': 'Verified data based on measurements'
                    },
                    {
                        'position': 2, 'label': '2',
                        'description': 'Verified data partly based on '
                                       'assumptions or non-verified data '
                                       'based on measurements'
                    },
                    {
                        'position': 3, 'label': '3',
                        'description': 'Non-verified data partly based on '
                                       'qualified estimates'
                    },
                    {
                        'position': 4, 'label': '4',
                        'description': 'Qualified estimate (e.g. by industrial '
                                       'expert)'
                    },
                    {
                        'position': 5, 'label': '5',
                        'description': 'Non-qualified estimates'
                    }
                ]
            },
            {
                'name': 'Completeness', 'position': 2,
                'scores': [
                    {
                        'position': 1, 'label': '1',
                        'description': 'Representative data from all sites '
                                       'relevant for the market considered, '
                                       'over and adequate period to even out '
                                       'normal fluctuations',
                    },
                    {
                        'position': 2, 'label': '2',
                        'description': 'Representative data from \u003e 50% of '
                                       'the sites relevant for the market '
                                       'considered, over an adequate period '
                                       'to even out normal fluctuations',
                    },
                    {
                        'position': 3, 'label': '3',
                        'description': 'Representative data from only some '
                                       'sites (\u003c\u003c 50%) relevant for '
                                       'the market considered or \u003e 50% of '
                                       'sites but from shorter periods',
                    },
                    {
                        'position': 4, 'label': '4',
                        'description': 'Representative data from only one site '
                                       'relevant for the market considered or '
                                       'some sites but from shorter periods',
                    },
                    {
                        'position': 5, 'label': '5',
                        'description': 'Representativeness unknown or data '
                                       'from a small number of sites and from '
                                       'shorter periods',
                    }
                ]
            }
        ]
    }
    return s
