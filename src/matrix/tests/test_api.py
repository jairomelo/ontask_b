# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os

import pandas as pd
from django.conf import settings
from django.shortcuts import reverse
from rest_framework.authtoken.models import Token

import test
from dataops import pandas_db
from matrix import serializers
from workflow.models import Workflow, Column
from workflow.ops import workflow_delete_column

class MatrixApiBase(test.OntaskApiTestCase):
    fixtures = ['simple_matrix']
    filename = os.path.join(
        settings.PROJECT_PATH,
        'matrix',
        'fixtures',
        'simple_matrix_df.sql'
    )

    new_matrix = {
        "email": ["student4@bogus.com",
                  "student5@bogus.com",
                  "student6@bogus.com"
                  ],
        "sid": [4, 5, 6],
        "age": [122.0, 122.1, 132.2],
        "another": ["bbbb", "aaab", "bbbb"],
        "name": ["Felipe Lotas", "Aitor Tilla", "Carmelo Coton"],
        "one": ["aaaa", "bbbb", "aaaa"],
        "registered": [True, False, True],
        "when": ["2017-10-12T00:33:44",
                 "2017-10-12T00:32:44",
                 "2017-10-12T00:32:44"
                 ]
    }

    src_df = {
        "sid": [1, 2, 4],
        "newcol": ['v1', 'v2', 'v3']
    }

    src_df2 = {
        "sid": [5],
        "forcenas": ['value']
    }

    def setUp(self):
        super(MatrixApiBase, self).setUp()
        # Get the token for authentication and set credentials in client
        token = Token.objects.get(user__email='idesigner1@bogus.com')
        auth = 'Token ' + token.key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        pandas_db.pg_restore_table(self.filename)

    def tearDown(self):
        pandas_db.delete_all_tables()
        super(MatrixApiBase, self).tearDown()


class MatrixApiCreate(MatrixApiBase):
    # Getting the matrix attached to the workflow
    def test_matrix_get(self):
        # Get the only workflow in the fixture
        workflow = Workflow.objects.all()[0]

        # Get the data through the API
        response = self.client.get(reverse('matrix:api_ops',
                                           kwargs={'pk': workflow.id}))

        # Transform the response into a data frame
        r_df = serializers.string_to_df(response.data['data_frame'])

        # Load the df from the db
        df = pandas_db.load_from_db(workflow.id)

        # Compare both elements
        self.compare_matrices(r_df, df)

    def test_matrix_try_overwrite(self):
        # Upload a matrix and try to overwrite an existing one (should fail)

        # Get the only workflow in the fixture
        workflow = Workflow.objects.all()[0]

        # Override the matrix
        response = self.client.post(reverse('matrix:api_ops',
                                            kwargs={'pk': workflow.id}),
                                    self.new_matrix,
                                    format='json')

        # Check that the right message is returned
        self.assertIn('Post request requires workflow without a matrix',
                      response.data['detail'])

    def test_matrix_create(self):
        # Create a second workflow
        response = self.client.post(reverse('workflow:api_workflows'),
                                    {'name': test.wflow_name + '2',
                                     'attributes': {'one': 'two'}},
                                    format='json')

        # Get the only workflow in the fixture
        workflow = Workflow.objects.get(pk=response.data['id'])

        # Transform new matrix into string
        r_df = pd.DataFrame(self.new_matrix)

        # Upload the matrix
        response = self.client.post(
            reverse('matrix:api_ops',
                    kwargs={'pk': workflow.id}),
            {'data_frame': serializers.df_to_string(r_df)},
            format='json')

        # Transform the response into a data frame
        r_df = serializers.string_to_df(response.data['data_frame'])

        # Load the df from the db
        df = pandas_db.load_from_db(workflow.id)

        # Compare both elements
        self.compare_matrices(r_df, df)

        # Refresh wflow (has been updated) and check that the rest of the
        # information is correct
        workflow = Workflow.objects.get(pk=workflow.id)
        self.assertTrue(pandas_db.check_wf_df(workflow))

    def test_matrix_update(self):
        # Get the only workflow in the fixture
        workflow = Workflow.objects.all()[0]

        # Transform new matrix into string
        r_df = pd.DataFrame(self.new_matrix)

        # Upload a new matrix
        response = self.client.put(
            reverse('matrix:api_ops',
                    kwargs={'pk': workflow.id}),
            {'data_frame': serializers.df_to_string(r_df)},
            format='json')

        # Transform the response into a data frame
        r_df = serializers.string_to_df(response.data['data_frame'])

        # Load the df from the db
        df = pandas_db.load_from_db(workflow.id)

        # Compare both elements
        self.compare_matrices(r_df, df)

        # Refresh wflow (has been updated) and check that the rest of the
        # information is correct
        workflow = Workflow.objects.get(pk=workflow.id)
        self.assertTrue(pandas_db.check_wf_df(workflow))

    def test_matrix_flush(self):
        # Get the only workflow in the fixture
        workflow = Workflow.objects.all()[0]

        # Flush the data in the matrix
        response = self.client.delete(reverse('matrix:api_ops',
                                              kwargs={'pk': workflow.id}))

        workflow = Workflow.objects.all()[0]
        self.assertTrue(pandas_db.check_wf_df(workflow))


class MatrixApiMerge(MatrixApiBase):
    # Getting the matrix through the merge API
    def test_matrix_merge_get(self):
        # Get the only workflow in the fixture
        workflow = Workflow.objects.all()[0]

        # Get the data through the API
        response = self.client.get(reverse('matrix:api_merge',
                                           kwargs={'pk': workflow.id}))

        # Transform new matrix into string
        r_df = serializers.string_to_df(response.data['src_df'])

        # Load the df from the db
        df = pandas_db.load_from_db(workflow.id)

        # Compare both elements and check wf df consistency
        self.compare_matrices(r_df, df)
        workflow = Workflow.objects.all()[0]
        self.assertTrue(pandas_db.check_wf_df(workflow))

    # Merge and create an empty dataset
    def test_matrix_merge_to_empty(self):
        # Get the only workflow in the fixture
        workflow = Workflow.objects.all()[0]

        # Transform new matrix into string
        r_df = pd.DataFrame(self.new_matrix)

        # Get the data through the API
        response = self.client.put(
            reverse('matrix:api_merge', kwargs={'pk': workflow.id}),
            {
                "src_df": serializers.df_to_string(r_df),
                "how": "inner",
                "left_on": "sid",
                "right_on": "sid",
                "dup_column": "override"
            },
            format='json')

        self.assertEqual(response.data['detail'],
                         'Merge operation produced a result with no rows')

        # Check for df/wf consistency
        workflow = Workflow.objects.all()[0]
        self.assertTrue(pandas_db.check_wf_df(workflow))

    # Merge with inner values
    def test_matrix_merge_to_inner(self):
        # Get the only workflow in the fixture
        workflow = Workflow.objects.all()[0]

        # Transform new matrix into string
        r_df = pd.DataFrame(self.src_df)

        # Get the data through the API
        response = self.client.put(
            reverse('matrix:api_merge', kwargs={'pk': workflow.id}),
            {
                "src_df": serializers.df_to_string(r_df),
                "how": "inner",
                "left_on": "sid",
                "right_on": "sid",
                "dup_column": "override"
            },
            format='json')

        # Get the updated object
        workflow = Workflow.objects.all()[0]

        # Result should have two rows
        self.assertEqual(workflow.nrows, 2)

        # Check for df/wf consistency
        self.assertTrue(pandas_db.check_wf_df(workflow))

    # Merge with outer values
    def test_matrix_merge_to_outer(self):
        # Get the only workflow in the fixture
        workflow = Workflow.objects.all()[0]

        # Transform new matrix into string
        r_df = pd.DataFrame(self.src_df)

        # Get the data through the API
        response = self.client.put(
            reverse('matrix:api_merge', kwargs={'pk': workflow.id}),
            {
                "src_df": serializers.df_to_string(r_df),
                "how": "outer",
                "left_on": "sid",
                "right_on": "sid",
                "dup_column": "override"
            },
            format='json')

        # Anomaly detected
        self.assertIn('New values in column', response.data['detail'])
        self.assertIn('are not of type', response.data['detail'])

        # Get the new workflow
        workflow = Workflow.objects.all()[0]

        # Result should have three rows as the initial DF
        self.assertEqual(workflow.nrows, 3)

        # Check for df/wf consistency
        self.assertTrue(pandas_db.check_wf_df(workflow))

    # Merge with left values
    def test_matrix_merge_to_left(self):
        # Get the only workflow in the fixture
        workflow = Workflow.objects.all()[0]

        # Transform new matrix into string
        r_df = pd.DataFrame(self.src_df)

        # Get the data through the API
        response = self.client.put(
            reverse('matrix:api_merge', kwargs={'pk': workflow.id}),
            {
                "src_df": serializers.df_to_string(r_df),
                "how": "left",
                "left_on": "sid",
                "right_on": "sid",
                "dup_column": "override"
            },
            format='json')

        # Get the new workflow
        workflow = Workflow.objects.all()[0]

        # Result should have three rows as the initial DF
        self.assertEqual(workflow.nrows, 3)

        df = pandas_db.load_from_db(workflow.id)
        self.assertEqual(df[df['sid'] == 1]['newcol'].values[0],
                         self.src_df['newcol'][0])

        # Check for df/wf consistency
        self.assertTrue(pandas_db.check_wf_df(workflow))

    # Merge with outer values but producing NaN everywhere
    def test_matrix_merge_to_outer_NaN(self):
        # Get the only workflow in the fixture
        workflow = Workflow.objects.all()[0]

        # Drop the column with booleans because the data type is lost
        workflow_delete_column(
            workflow,
            Column.objects.get(
                workflow=workflow,
                name='registered'
            )
        )

        # Transform new matrix into string
        r_df = pd.DataFrame(self.src_df2)

        # Load the df from the db
        df = pandas_db.load_from_db(workflow.id)
        new_df = pd.merge(df, r_df, how="outer", left_on="sid", right_on="sid")

        # Get the data through the API
        response = self.client.put(
            reverse('matrix:api_merge', kwargs={'pk': workflow.id}),
            {
                "src_df": serializers.df_to_string(r_df),
                "how": "outer",
                "left_on": "sid",
                "right_on": "sid",
                "dup_column": "override"
            },
            format='json')

        # Get the new workflow
        workflow = Workflow.objects.all()[0]

        # Result should have three rows as the initial DF
        self.assertEqual(workflow.nrows, 4)
        self.assertEqual(workflow.ncols, 8)

        # Load the df from the db
        df = pandas_db.load_from_db(workflow.id)

        # Compare both elements and check wf df consistency
        self.compare_matrices(df, new_df)

        # Check for df/wf consistency
        self.assertTrue(pandas_db.check_wf_df(workflow))
