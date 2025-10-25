from django.test import TestCase
from django.urls import reverse
from drivecar.models import Veiculo

class VeiculoViewTests(TestCase):
    def setUp(self):
        self.url = reverse('drivecar:cadastrar_veiculo')
        self.index_url = reverse('drivecar:index')
        self.data = {
            'marca': 'TestMarca',
            'modelo': 'TestModelo',
            'ano': 2020,
            'placa': 'ABC1234',
            'km_atual': 1000,
            'combustivel': 'Gasolina',
        }

    def test_cadastrar_veiculo_normal_post_redirects(self):
        resp = self.client.post(self.url, data=self.data)
        # espera redirect padrão
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, self.index_url)
        self.assertEqual(Veiculo.objects.count(), 1)

    def test_cadastrar_veiculo_htmx_post_returns_hx_redirect_header(self):
        # Simula requisição HTMX definindo header HX-Request
        resp = self.client.post(self.url, data=self.data, **{'HTTP_HX_REQUEST': 'true'})
        # Para HTMX esperamos um 200 (HttpResponse) com header HX-Redirect
        self.assertEqual(resp.status_code, 200)
        self.assertIn('HX-Redirect', resp)
        self.assertEqual(resp['HX-Redirect'], self.index_url)
        self.assertEqual(Veiculo.objects.count(), 1)
