import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData
from scipy.optimize import minimize
from scipy.optimize import approx_fprime
from scipy.stats import chi2

# Função do modelo para o ajuste
def falling_time_model(B, t):
    g = B[0]  # parâmetro da gravidade
    return 0.5 * g * t**2

# Função de verossimilhança negativa
def negative_log_likelihood(g, t, y, yerr):
    model = 0.5 * g * t**2
    chi2 = ((y - model) / yerr) ** 2
    return 0.5 * np.sum(chi2)

# Função para calcular a matriz Hessiana
def calculate_hessian(g, t, y, yerr, epsilon=1e-8):
    n_params = len(g)
    hessian = np.zeros((n_params, n_params))
    for i in range(n_params):
        params_plus = np.copy(g)
        params_minus = np.copy(g)
        params_plus[i] += epsilon
        params_minus[i] -= epsilon
        grad_plus = approx_fprime(params_plus, negative_log_likelihood, epsilon, t, y, yerr)
        grad_minus = approx_fprime(params_minus, negative_log_likelihood, epsilon, t, y, yerr)
        hessian[:, i] = (grad_plus - grad_minus) / (2 * epsilon)
    return hessian

# Carrega os dados
df = pd.read_csv('resultados_quedalivre.csv')

# Extraindo dados
position = df['Posição (m)'].values
time_mean = df['Média (s)'].values
time_std = df['Desvio Padrão da Média (s)'].values

# Incerteza na posição
position_err = np.full_like(position, 0.1)

# Prepara os dados para o ODR
data = RealData(time_mean, position, sx=time_std, sy=position_err)
model = Model(falling_time_model)
odr = ODR(data, model, beta0=[9.81])

# Executa o ajuste ODR
output = odr.run()
g_fit_odr = output.beta[0]
g_err_odr = output.sd_beta[0]
chi2_odr = output.sum_square
degrees_of_freedom_odr = len(position) - len(output.beta)

# Gráfico do ajuste ODR
plt.figure()
plt.errorbar(time_mean, position, xerr=time_std, yerr=position_err, fmt='o', label='Dados')
t_fit = np.linspace(min(time_mean), max(time_mean), 100)
plt.plot(t_fit, falling_time_model([g_fit_odr], t_fit), label=f'Ajuste ODR: g = {g_fit_odr:.3f} ± {g_err_odr:.3f} m/s²\nχ² = {chi2_odr:.2f}\nGL = {degrees_of_freedom_odr}')
plt.xlabel('Tempo Médio (s)')
plt.ylabel('Posição (m)')
plt.legend()
plt.title('Ajuste com ODR')
plt.savefig('ajuste_odr.png')
plt.close()

# Ajuste com log-máxima verossimilhança
result_mle = minimize(negative_log_likelihood, x0=[9.81], args=(time_mean, position, position_err), method='BFGS')
g_fit_mle = result_mle.x[0]
log_likelihood = -result_mle.fun

# Matriz Hessiana e incertezas
hessian = calculate_hessian(result_mle.x, time_mean, position, position_err)
cov_matrix = np.linalg.inv(hessian)
g_err_mle = np.sqrt(np.diag(cov_matrix))

# Gráfico do ajuste MLE
plt.figure()
plt.errorbar(time_mean, position, xerr=time_std, yerr=position_err, fmt='o', label='Dados')
plt.plot(t_fit, falling_time_model([g_fit_mle], t_fit), label=f'Ajuste MLE: g = {g_fit_mle:.3f} ± {g_err_mle[0]:.3f} m/s²\nLog-Likelihood = {log_likelihood:.2f}')
plt.xlabel('Tempo Médio (s)')
plt.ylabel('Posição (m)')
plt.legend()
plt.title('Ajuste com Log-Máxima Verossimilhança')
plt.savefig('ajuste_mle.png')
plt.close()

# Teste de Razão de Verossimilhança
log_likelihood_null = -negative_log_likelihood(9.81, time_mean, position, position_err)  # Modelo nulo com g = 9.81
lr_statistic = -2 * (log_likelihood_null - log_likelihood)
p_value = chi2.sf(lr_statistic, df=1)

# Exibindo resultados do teste de razão de verossimilhança
print(f"Log-Likelihood do modelo nulo: {log_likelihood_null:.2f}")
print(f"Log-Likelihood do modelo ajustado: {log_likelihood:.2f}")
print(f"Estatística do Teste de Razão de Verossimilhança: {lr_statistic:.2f}")
print(f"P-Valor: {p_value:.5f}")
print(f"Incerteza da gravidade (MLE): {g_err_mle[0]:.3f}")

# Salvando os resultados em um arquivo de texto
with open('resultados_ajuste.txt', 'w') as f:
    f.write(f"Ajuste ODR: g = {g_fit_odr:.3f} ± {g_err_odr:.3f} m/s²\n")
    f.write(f"χ² = {chi2_odr:.2f}, GL = {degrees_of_freedom_odr}\n")
    f.write(f"Ajuste MLE: g = {g_fit_mle:.3f} ± {g_err_mle[0]:.3f} m/s²\n")
    f.write(f"Log-Likelihood = {log_likelihood:.2f}\n")
    f.write(f"Estatística do Teste de Razão de Verossimilhança: {lr_statistic:.2f}\n")
    f.write(f"P-Valor: {p_value:.5f}\n")
